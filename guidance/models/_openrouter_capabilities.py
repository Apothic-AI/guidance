import json
import threading
import time
from typing import Any, Literal
from urllib import error as urllib_error
from urllib import parse as urllib_parse
from urllib import request as urllib_request

_OPENROUTER_ENDPOINTS_TTL_SECONDS = 300.0
_OPENROUTER_ENDPOINTS_FAILURE_TTL_SECONDS = 60.0
_OPENROUTER_ENDPOINTS_CACHE: dict[tuple[str, str], tuple[float, list[dict[str, Any]]]] = {}
_OPENROUTER_ENDPOINTS_CACHE_LOCK = threading.Lock()
_OPENROUTER_MODELS_TTL_SECONDS = 3600.0
_OPENROUTER_MODELS_FAILURE_TTL_SECONDS = 60.0
_OPENROUTER_MODELS_CACHE: dict[tuple[str, str], tuple[float, dict[str, dict[str, Any]]]] = {}
_OPENROUTER_MODELS_CACHE_LOCK = threading.Lock()
_DEFAULT_OPENROUTER_API_BASE = "https://openrouter.ai/api/v1"
_OPENROUTER_TOP_LOGPROBS_SAFE_MAX = 20
_OPENROUTER_PROVIDER_GRAMMAR_FORMAT_HINTS: dict[str, Literal["ll-lark", "gbnf"]] = {
    "fireworks": "gbnf",
}


def _normalized_openrouter_api_base(raw_base: str | None) -> str:
    base = str(raw_base or "").strip().lower()
    if not base:
        return _DEFAULT_OPENROUTER_API_BASE
    marker = "/api/v1"
    idx = base.find(marker)
    if idx >= 0:
        return base[: idx + len(marker)]
    return base.rstrip("/")


def _normalized_openrouter_model_name(model: str) -> str:
    return str(model).strip().strip("/").lower()


def _openrouter_model_aliases(model: str) -> list[str]:
    normalized = _normalized_openrouter_model_name(model)
    if not normalized:
        return []
    aliases = [normalized]
    if ":" in normalized:
        aliases.append(normalized.split(":", 1)[0])
    return aliases


def _extract_openrouter_supported_parameters(model_meta: dict[str, Any] | None) -> set[str]:
    if not isinstance(model_meta, dict):
        return set()
    raw_supported = model_meta.get("supported_parameters")
    if not isinstance(raw_supported, list):
        return set()
    return {str(item).strip().lower() for item in raw_supported if str(item).strip()}


def _extract_openrouter_model_modalities(model_meta: dict[str, Any] | None) -> tuple[set[str], set[str]]:
    if not isinstance(model_meta, dict):
        return set(), set()
    architecture = model_meta.get("architecture")
    if not isinstance(architecture, dict):
        return set(), set()

    def _to_modalities(value: Any) -> set[str]:
        if not isinstance(value, list):
            return set()
        return {str(item).strip().lower() for item in value if str(item).strip()}

    return _to_modalities(architecture.get("input_modalities")), _to_modalities(architecture.get("output_modalities"))


def fetch_openrouter_models_catalog(
    *,
    api_base: str,
    api_key: str = "",
) -> dict[str, dict[str, Any]]:
    """Fetch and cache OpenRouter's model catalog from /models."""
    normalized_base = _normalized_openrouter_api_base(api_base)
    key = str(api_key or "").strip()
    cache_key = (normalized_base, key)
    now = time.time()
    with _OPENROUTER_MODELS_CACHE_LOCK:
        cached = _OPENROUTER_MODELS_CACHE.get(cache_key)
        if cached and cached[0] > now:
            return dict(cached[1])

    headers = {"Accept": "application/json"}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    request = urllib_request.Request(f"{normalized_base}/models", headers=headers)

    ttl = _OPENROUTER_MODELS_FAILURE_TTL_SECONDS
    catalog: dict[str, dict[str, Any]] = {}
    try:
        with urllib_request.urlopen(request, timeout=6) as response:  # noqa: S310
            payload = json.loads(response.read().decode("utf-8"))
        data = payload.get("data") if isinstance(payload, dict) else None
        rows = data if isinstance(data, list) else []
        for row in rows:
            if not isinstance(row, dict):
                continue
            model_id = _normalized_openrouter_model_name(str(row.get("id", "")))
            canonical_slug = _normalized_openrouter_model_name(str(row.get("canonical_slug", "")))
            if model_id:
                catalog[model_id] = row
            if canonical_slug:
                catalog.setdefault(canonical_slug, row)
        ttl = _OPENROUTER_MODELS_TTL_SECONDS
    except (urllib_error.URLError, urllib_error.HTTPError, TimeoutError, json.JSONDecodeError):
        catalog = {}

    with _OPENROUTER_MODELS_CACHE_LOCK:
        _OPENROUTER_MODELS_CACHE[cache_key] = (now + ttl, dict(catalog))
    return catalog


def resolve_openrouter_model_metadata(
    *,
    model: str,
    api_base: str,
    api_key: str = "",
) -> dict[str, Any] | None:
    catalog = fetch_openrouter_models_catalog(api_base=api_base, api_key=api_key)
    for alias in _openrouter_model_aliases(model):
        if alias in catalog:
            return catalog[alias]
    return None


class OpenRouterCapabilityMixin:
    model: str
    client: Any
    reasoning_effort: str | None
    openrouter_require_parameters: bool | None
    openrouter_allow_fallbacks: bool | None
    openrouter_provider: str | None

    def _client_base_url(self) -> str:
        raw_base: Any = None
        for obj in (self.client, getattr(self.client, "client", None)):
            if obj is None:
                continue
            for attr in ("base_url", "server_url", "api_base"):
                value = getattr(obj, attr, None)
                if value:
                    raw_base = value
                    break
            if raw_base:
                break
        return str(raw_base or "").strip().lower()

    def _is_openrouter_client(self) -> bool:
        return "openrouter.ai" in self._client_base_url()

    def _openrouter_client_api_key(self) -> str:
        raw_key: Any = ""
        for obj in (self.client, getattr(self.client, "client", None)):
            if obj is None:
                continue
            candidate = getattr(obj, "api_key", "")
            if candidate:
                raw_key = candidate
                break
        if hasattr(raw_key, "get_secret_value"):
            try:
                raw_key = raw_key.get_secret_value()
            except Exception:  # noqa: BLE001
                raw_key = ""
        key = str(raw_key).strip()
        if not key or key.startswith("*"):
            return ""
        return key

    def _openrouter_api_base(self) -> str:
        base = _normalized_openrouter_api_base(self._client_base_url())
        return base if base else _DEFAULT_OPENROUTER_API_BASE

    def _openrouter_model_metadata(self, model: str | None = None) -> dict[str, Any] | None:
        return resolve_openrouter_model_metadata(
            model=self.model if model is None else model,
            api_base=self._openrouter_api_base(),
            api_key=self._openrouter_client_api_key(),
        )

    def _openrouter_model_supported_parameters(self, model: str | None = None) -> set[str]:
        return _extract_openrouter_supported_parameters(self._openrouter_model_metadata(model))

    def _openrouter_model_modalities(self, model: str | None = None) -> tuple[set[str], set[str]]:
        return _extract_openrouter_model_modalities(self._openrouter_model_metadata(model))

    def _openrouter_supports_input_modality(self, modality: str) -> bool:
        input_modalities, _ = self._openrouter_model_modalities()
        return str(modality).strip().lower() in input_modalities

    def _openrouter_supports_output_modality(self, modality: str) -> bool:
        _, output_modalities = self._openrouter_model_modalities()
        return str(modality).strip().lower() in output_modalities

    def _openrouter_model_endpoints_url(self, model: str) -> str:
        model_text = str(model).strip().strip("/")
        if not model_text:
            return ""
        base = self._openrouter_api_base()
        if "/" in model_text:
            author, slug = model_text.split("/", 1)
            author_token = urllib_parse.quote(author, safe="")
            slug_token = urllib_parse.quote(slug, safe="")
            return f"{base}/models/{author_token}/{slug_token}/endpoints"
        model_token = urllib_parse.quote(model_text, safe="")
        return f"{base}/models/{model_token}/endpoints"

    def _openrouter_fetch_model_endpoints(self, model: str) -> list[dict[str, Any]]:
        url = self._openrouter_model_endpoints_url(model)
        if not url:
            return []
        cache_key = (self._openrouter_api_base(), _normalized_openrouter_model_name(model))
        now = time.time()
        with _OPENROUTER_ENDPOINTS_CACHE_LOCK:
            cached = _OPENROUTER_ENDPOINTS_CACHE.get(cache_key)
            if cached and cached[0] > now:
                return list(cached[1])

        headers = {"Accept": "application/json"}
        api_key = self._openrouter_client_api_key()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        request = urllib_request.Request(url, headers=headers)

        ttl = _OPENROUTER_ENDPOINTS_FAILURE_TTL_SECONDS
        endpoints: list[dict[str, Any]] = []
        try:
            with urllib_request.urlopen(request, timeout=6) as response:  # noqa: S310
                payload = json.loads(response.read().decode("utf-8"))
            data = payload.get("data") if isinstance(payload, dict) else None
            raw_endpoints = data.get("endpoints") if isinstance(data, dict) else None
            if isinstance(raw_endpoints, list):
                endpoints = [row for row in raw_endpoints if isinstance(row, dict)]
            ttl = _OPENROUTER_ENDPOINTS_TTL_SECONDS
        except (urllib_error.URLError, urllib_error.HTTPError, TimeoutError, json.JSONDecodeError):
            endpoints = []

        with _OPENROUTER_ENDPOINTS_CACHE_LOCK:
            _OPENROUTER_ENDPOINTS_CACHE[cache_key] = (now + ttl, list(endpoints))
        return endpoints

    def _openrouter_provider_settings(self, request_kwargs: dict[str, Any]) -> tuple[list[str], bool]:
        extra = request_kwargs.get("extra_body")
        if not isinstance(extra, dict):
            return [], False
        provider = extra.get("provider")
        if not isinstance(provider, dict):
            return [], False
        order_raw = provider.get("order")
        order: list[str] = []
        if isinstance(order_raw, list):
            for item in order_raw:
                text = str(item).strip().lower()
                if text:
                    order.append(text)
        require_parameters = bool(provider.get("require_parameters", False))
        return order, require_parameters

    def _openrouter_apply_constraint_routing_defaults(
        self,
        request_kwargs: dict[str, Any],
        *,
        require_parameters: bool = True,
        allow_fallbacks: bool = False,
    ) -> dict[str, Any]:
        """Bias constrained requests toward capability-compatible providers."""
        normalized = dict(request_kwargs)
        raw_extra = normalized.get("extra_body")
        extra_body = dict(raw_extra) if isinstance(raw_extra, dict) else {}

        provider = extra_body.get("provider")
        provider_obj = dict(provider) if isinstance(provider, dict) else {}
        provider_obj.setdefault("require_parameters", bool(require_parameters))
        provider_obj.setdefault("allow_fallbacks", bool(allow_fallbacks))
        extra_body["provider"] = provider_obj
        normalized["extra_body"] = extra_body
        return normalized

    def _openrouter_candidate_endpoints(
        self,
        *,
        endpoints: list[dict[str, Any]],
        provider_order: list[str],
    ) -> list[dict[str, Any]]:
        if not provider_order:
            return list(endpoints)
        filtered: list[dict[str, Any]] = []
        for endpoint in endpoints:
            provider_name = str(endpoint.get("provider_name", "")).strip().lower()
            tag = str(endpoint.get("tag", "")).strip().lower()
            name = str(endpoint.get("name", "")).strip().lower()
            haystack = " ".join((provider_name, tag, name))
            if any(token == provider_name or token == tag or token in haystack for token in provider_order):
                filtered.append(endpoint)
        return filtered if filtered else list(endpoints)

    def _openrouter_parameter_supported(
        self,
        *,
        endpoints: list[dict[str, Any]],
        parameter: str,
        require_parameters: bool,
    ) -> bool:
        if not endpoints:
            return False
        supported_count = 0
        for endpoint in endpoints:
            supported = endpoint.get("supported_parameters")
            if not isinstance(supported, list):
                continue
            if parameter in {str(item).strip() for item in supported}:
                supported_count += 1
        if supported_count <= 0:
            return False
        if require_parameters:
            return True
        return supported_count == len(endpoints)

    def _openrouter_parameter_supported_for_request(
        self,
        *,
        request_kwargs: dict[str, Any],
        parameter: str,
    ) -> bool:
        parameter_name = str(parameter).strip().lower()
        if not parameter_name:
            return False

        provider_order, require_parameters = self._openrouter_provider_settings(request_kwargs)
        model_supported = self._openrouter_model_supported_parameters()

        # Prefer the global model catalog unless the caller constrained provider routing.
        if model_supported and not provider_order:
            return parameter_name in model_supported

        endpoints = self._openrouter_fetch_model_endpoints(self.model)
        candidates = self._openrouter_candidate_endpoints(
            endpoints=endpoints,
            provider_order=provider_order,
        )
        if candidates:
            return self._openrouter_parameter_supported(
                endpoints=candidates,
                parameter=parameter_name,
                require_parameters=require_parameters,
            )
        return parameter_name in model_supported

    def _openrouter_logprobs_capability(self, request_kwargs: dict[str, Any]) -> tuple[bool, bool]:
        supports_logprobs = self._openrouter_parameter_supported_for_request(
            request_kwargs=request_kwargs,
            parameter="logprobs",
        )
        supports_top_logprobs = self._openrouter_parameter_supported_for_request(
            request_kwargs=request_kwargs,
            parameter="top_logprobs",
        )
        return supports_logprobs, supports_top_logprobs

    def _openrouter_normalized_top_logprobs(self, value: Any) -> int | None:
        if value is None:
            return None
        try:
            parsed = int(value)
        except (TypeError, ValueError):
            return None
        if parsed <= 0:
            return None
        return min(parsed, _OPENROUTER_TOP_LOGPROBS_SAFE_MAX)

    def _openrouter_effective_logprobs_mode(
        self,
        *,
        request_kwargs: dict[str, Any],
        enable_logprobs: bool,
        top_logprobs: Any,
    ) -> tuple[Literal["disabled", "logprobs_only", "logprobs_and_top_logprobs"], int | None]:
        if not enable_logprobs:
            return "disabled", None

        supports_logprobs, supports_top_logprobs = self._openrouter_logprobs_capability(request_kwargs)
        if not supports_logprobs:
            return "disabled", None

        normalized_top_logprobs = self._openrouter_normalized_top_logprobs(top_logprobs)
        if normalized_top_logprobs is None or not supports_top_logprobs:
            return "logprobs_only", None
        return "logprobs_and_top_logprobs", normalized_top_logprobs

    def _openrouter_supports_tools(self, request_kwargs: dict[str, Any]) -> bool:
        return self._openrouter_parameter_supported_for_request(
            request_kwargs=request_kwargs,
            parameter="tools",
        )

    def _openrouter_supports_response_format(self, request_kwargs: dict[str, Any]) -> bool:
        return self._openrouter_parameter_supported_for_request(
            request_kwargs=request_kwargs,
            parameter="response_format",
        ) or self._openrouter_parameter_supported_for_request(
            request_kwargs=request_kwargs,
            parameter="structured_outputs",
        )

    def _openrouter_supports_grammar_response_format(self, request_kwargs: dict[str, Any]) -> bool:
        # `structured_outputs` in model metadata implies JSON schema capability, not necessarily free-form grammar.
        return self._openrouter_parameter_supported_for_request(
            request_kwargs=request_kwargs,
            parameter="response_format",
        )

    def _openrouter_grammar_format_for_request(self, request_kwargs: dict[str, Any]) -> Literal["ll-lark", "gbnf"]:
        provider_order, _ = self._openrouter_provider_settings(request_kwargs)
        if provider_order:
            first = provider_order[0].strip().lower()
            for marker, grammar_format in _OPENROUTER_PROVIDER_GRAMMAR_FORMAT_HINTS.items():
                if first == marker or marker in first:
                    return grammar_format
        return "ll-lark"

    def _openrouter_supports_reasoning(self, request_kwargs: dict[str, Any]) -> bool:
        return self._openrouter_parameter_supported_for_request(
            request_kwargs=request_kwargs,
            parameter="reasoning",
        ) or self._openrouter_parameter_supported_for_request(
            request_kwargs=request_kwargs,
            parameter="reasoning_effort",
        )

    def _openrouter_filter_optional_parameters(self, request_kwargs: dict[str, Any]) -> dict[str, Any]:
        normalized = dict(request_kwargs)
        for request_key, parameter in (
            ("top_p", "top_p"),
            ("top_k", "top_k"),
            ("min_p", "min_p"),
            ("repetition_penalty", "repetition_penalty"),
        ):
            if request_key in normalized and not self._openrouter_parameter_supported_for_request(
                request_kwargs=normalized,
                parameter=parameter,
            ):
                normalized.pop(request_key, None)
        return normalized

    def _openrouter_effective_reasoning_effort(self, request_kwargs: dict[str, Any]) -> str | None:
        explicit = request_kwargs.pop("reasoning_effort", None)
        if isinstance(explicit, str) and explicit.strip():
            return explicit.strip()
        if isinstance(self.reasoning_effort, str) and self.reasoning_effort.strip():
            return self.reasoning_effort.strip()
        return None

    def _apply_openrouter_request_overrides(self, request_kwargs: dict[str, Any]) -> dict[str, Any]:
        normalized = dict(request_kwargs)

        if "max_completion_tokens" in normalized and "max_tokens" not in normalized:
            normalized["max_tokens"] = normalized.get("max_completion_tokens")
        normalized.pop("max_completion_tokens", None)

        raw_extra = normalized.get("extra_body")
        extra_body = dict(raw_extra) if isinstance(raw_extra, dict) else {}

        provider = extra_body.get("provider")
        provider_obj = dict(provider) if isinstance(provider, dict) else {}
        if self.openrouter_require_parameters is not None:
            provider_obj.setdefault("require_parameters", bool(self.openrouter_require_parameters))
        if self.openrouter_allow_fallbacks is not None:
            provider_obj.setdefault("allow_fallbacks", bool(self.openrouter_allow_fallbacks))
        if isinstance(self.openrouter_provider, str) and self.openrouter_provider.strip():
            provider_obj.setdefault("order", [self.openrouter_provider.strip()])
        if provider_obj:
            extra_body["provider"] = provider_obj

        reasoning_effort = self._openrouter_effective_reasoning_effort(normalized)
        capability_probe_kwargs = dict(normalized)
        if extra_body:
            capability_probe_kwargs["extra_body"] = extra_body
        if reasoning_effort and self._openrouter_supports_reasoning(capability_probe_kwargs):
            reasoning = extra_body.get("reasoning")
            reasoning_obj = dict(reasoning) if isinstance(reasoning, dict) else {}
            reasoning_obj.setdefault("effort", reasoning_effort)
            extra_body["reasoning"] = reasoning_obj

        if extra_body:
            normalized["extra_body"] = extra_body
        return self._openrouter_filter_optional_parameters(normalized)
