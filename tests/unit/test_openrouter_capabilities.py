import json
from typing import Any, Iterator

from guidance.models import _openai_base, _openrouter_capabilities


class _FakeResponse:
    def __init__(self, payload: dict[str, Any]):
        self._payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self) -> bytes:
        return json.dumps(self._payload).encode("utf-8")


def test_openrouter_models_catalog_is_cached(monkeypatch):
    calls = {"count": 0}
    payload = {
        "data": [
            {
                "id": "openai/gpt-4o-mini",
                "canonical_slug": "openai/gpt-4o-mini-2024-07-18",
                "supported_parameters": ["response_format", "tools"],
                "architecture": {"input_modalities": ["text", "image"], "output_modalities": ["text"]},
            }
        ]
    }

    def fake_urlopen(*args, **kwargs):  # noqa: ANN002, ANN003
        calls["count"] += 1
        return _FakeResponse(payload)

    monkeypatch.setattr(_openrouter_capabilities.urllib_request, "urlopen", fake_urlopen)
    _openrouter_capabilities._OPENROUTER_MODELS_CACHE.clear()

    first = _openrouter_capabilities.fetch_openrouter_models_catalog(
        api_base="https://openrouter.ai/api/v1",
        api_key="",
    )
    second = _openrouter_capabilities.fetch_openrouter_models_catalog(
        api_base="https://openrouter.ai/api/v1",
        api_key="",
    )

    assert calls["count"] == 1
    assert "openai/gpt-4o-mini" in first
    assert "openai/gpt-4o-mini-2024-07-18" in second


def test_openrouter_model_metadata_resolves_variant_suffix(monkeypatch):
    payload = {
        "data": [
            {
                "id": "openai/gpt-4o-mini",
                "canonical_slug": "openai/gpt-4o-mini-2024-07-18",
                "supported_parameters": ["response_format", "tools"],
            }
        ]
    }

    def fake_urlopen(*args, **kwargs):  # noqa: ANN002, ANN003
        return _FakeResponse(payload)

    monkeypatch.setattr(_openrouter_capabilities.urllib_request, "urlopen", fake_urlopen)
    _openrouter_capabilities._OPENROUTER_MODELS_CACHE.clear()

    meta = _openrouter_capabilities.resolve_openrouter_model_metadata(
        model="openai/gpt-4o-mini:free",
        api_base="https://openrouter.ai/api/v1",
        api_key="",
    )
    assert meta is not None
    assert meta["id"] == "openai/gpt-4o-mini"


class _DummyClientWrapper(_openai_base.BaseOpenAIClientWrapper):
    def __init__(self):
        self.base_url = "https://openrouter.ai/api/v1"
        self.api_key = "test-key"

    def streaming_chat_completions(  # noqa: ANN201
        self,
        model: str,
        messages: list[dict[str, Any]],
        logprobs: bool,
        **kwargs,
    ) -> Iterator[Any]:
        raise NotImplementedError


def test_openrouter_parameter_support_uses_model_metadata_without_provider_constraints(monkeypatch):
    interpreter = _openai_base.BaseOpenAIInterpreter(
        model="openai/gpt-4o-mini",
        client=_DummyClientWrapper(),
        reasoning_effort=None,
    )
    monkeypatch.setattr(
        interpreter,
        "_openrouter_model_supported_parameters",
        lambda model=None: {"top_p", "top_k", "tools", "response_format"},
    )

    def fail_if_called(model: str):
        raise AssertionError(f"unexpected endpoint fetch for {model}")

    monkeypatch.setattr(interpreter, "_openrouter_fetch_model_endpoints", fail_if_called)

    assert interpreter._openrouter_parameter_supported_for_request(request_kwargs={}, parameter="top_k")
    assert interpreter._openrouter_supports_tools({})
    assert interpreter._openrouter_supports_response_format({})
