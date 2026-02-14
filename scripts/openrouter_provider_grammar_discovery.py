#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal
from urllib import error as urllib_error
from urllib import parse as urllib_parse
from urllib import request as urllib_request

from guidance._ast import RegexNode
from guidance.models._grammar_support import FireworksGBNFBuilder

DEFAULT_OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_FORMATS = ("ll-lark", "gbnf")


@dataclass
class ProbeResult:
    model: str
    provider: str
    grammar_format: str
    outcome: Literal["reject", "accepts+obeys", "accepts+ignores"]
    status_code: int | None
    generated_text: str | None
    detail: str


def _normalize_api_base(raw_base: str | None) -> str:
    base = str(raw_base or "").strip()
    if not base:
        return DEFAULT_OPENROUTER_BASE_URL
    marker = "/api/v1"
    idx = base.lower().find(marker)
    if idx >= 0:
        return base[: idx + len(marker)]
    return base.rstrip("/")


def _normalize_model_name(model: str) -> str:
    return str(model).strip().strip("/").lower()


def _normalize_provider_name(provider: str) -> str:
    return str(provider).strip().lower()


def _split_csv(value: str | None) -> list[str]:
    text = str(value or "")
    return [item.strip() for item in text.split(",") if item.strip()]


def _model_endpoints_url(api_base: str, model: str) -> str:
    model_text = str(model).strip().strip("/")
    if "/" in model_text:
        author, slug = model_text.split("/", 1)
        return f"{api_base}/models/{urllib_parse.quote(author, safe='')}/{urllib_parse.quote(slug, safe='')}/endpoints"
    return f"{api_base}/models/{urllib_parse.quote(model_text, safe='')}/endpoints"


def _http_json(
    *,
    method: str,
    url: str,
    api_key: str,
    payload: dict[str, Any] | None = None,
    timeout_seconds: float,
) -> tuple[int, dict[str, Any] | None, str]:
    headers = {"Accept": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    body = None
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = urllib_request.Request(url=url, method=method, data=body, headers=headers)
    try:
        with urllib_request.urlopen(request, timeout=timeout_seconds) as response:  # noqa: S310
            raw_text = response.read().decode("utf-8")
            parsed = json.loads(raw_text) if raw_text else {}
            return int(getattr(response, "status", 200)), parsed if isinstance(parsed, dict) else None, raw_text
    except urllib_error.HTTPError as exc:
        raw_text = exc.read().decode("utf-8")
        parsed: dict[str, Any] | None = None
        try:
            decoded = json.loads(raw_text) if raw_text else {}
            if isinstance(decoded, dict):
                parsed = decoded
        except json.JSONDecodeError:
            parsed = None
        return int(exc.code), parsed, raw_text
    except urllib_error.URLError as exc:
        return 0, None, str(exc)


def fetch_provider_names(*, api_base: str, api_key: str, model: str, timeout_seconds: float) -> list[str]:
    url = _model_endpoints_url(api_base, model)
    status, parsed, _ = _http_json(
        method="GET",
        url=url,
        api_key=api_key,
        payload=None,
        timeout_seconds=timeout_seconds,
    )
    if status < 200 or status >= 300 or not parsed:
        return []
    data = parsed.get("data")
    if not isinstance(data, dict):
        return []
    endpoints = data.get("endpoints")
    if not isinstance(endpoints, list):
        return []
    providers: list[str] = []
    seen: set[str] = set()
    for endpoint in endpoints:
        if not isinstance(endpoint, dict):
            continue
        provider = str(endpoint.get("provider_name", "")).strip()
        key = _normalize_provider_name(provider)
        if not provider or key in seen:
            continue
        seen.add(key)
        providers.append(provider)
    return providers


def _extract_content_text(payload: dict[str, Any] | None) -> str | None:
    if not isinstance(payload, dict):
        return None
    choices = payload.get("choices")
    if not isinstance(choices, list) or not choices:
        return None
    choice = choices[0]
    if not isinstance(choice, dict):
        return None
    message = choice.get("message")
    if not isinstance(message, dict):
        return None
    content = message.get("content")
    if isinstance(content, str):
        if content:
            return content
    if isinstance(content, list):
        text_chunks: list[str] = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                text = item.get("text")
                if isinstance(text, str):
                    text_chunks.append(text)
        if text_chunks:
            return "".join(text_chunks)
    reasoning_content = message.get("reasoning_content")
    if isinstance(reasoning_content, str):
        return reasoning_content
    return None


def _classify_outcome(status_code: int, generated_text: str | None) -> tuple[str, str]:
    if status_code < 200 or status_code >= 300:
        return "reject", "provider rejected grammar request"

    text = (generated_text or "").strip()
    if text in {"YES", "NO"}:
        return "accepts+obeys", "output satisfies YES|NO"
    if text:
        return "accepts+ignores", "provider accepted request but returned unconstrained text"
    return "accepts+ignores", "provider accepted request but returned empty/non-text output"


def _extract_error_message(payload: dict[str, Any] | None) -> str | None:
    if not isinstance(payload, dict):
        return None
    err = payload.get("error")
    if isinstance(err, str):
        text = err.strip()
        return text or None
    if isinstance(err, dict):
        message = err.get("message")
        if isinstance(message, str) and message.strip():
            return message.strip()
        code = err.get("code")
        if code is not None:
            return f"provider returned error code {code}"
    return None


def probe_provider(
    *,
    api_base: str,
    api_key: str,
    model: str,
    provider: str,
    grammar_format: str,
    grammar: str,
    timeout_seconds: float,
) -> ProbeResult:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are concise."},
            {"role": "user", "content": "Reply with MAYBE only."},
        ],
        "max_tokens": 8,
        "temperature": 0,
        "provider": {
            "order": [provider],
            "allow_fallbacks": False,
            "require_parameters": True,
        },
        "response_format": {"type": "grammar", "grammar": grammar},
    }
    status, parsed, raw_text = _http_json(
        method="POST",
        url=f"{api_base}/chat/completions",
        api_key=api_key,
        payload=payload,
        timeout_seconds=timeout_seconds,
    )
    error_message = _extract_error_message(parsed)
    if error_message:
        return ProbeResult(
            model=model,
            provider=provider,
            grammar_format=grammar_format,
            outcome="reject",
            status_code=status if status > 0 else None,
            generated_text=None,
            detail=f"provider rejected grammar request: {error_message}",
        )
    generated = _extract_content_text(parsed)
    outcome, detail = _classify_outcome(status, generated)
    if outcome == "reject":
        reason = ""
        if isinstance(parsed, dict):
            error = parsed.get("error")
            if isinstance(error, dict):
                message = error.get("message")
                if isinstance(message, str):
                    reason = message
            elif isinstance(error, str):
                reason = error
        if not reason:
            reason = raw_text[:240].replace("\n", " ")
        detail = f"{detail}: {reason}"
    return ProbeResult(
        model=model,
        provider=provider,
        grammar_format=grammar_format,
        outcome=outcome,  # type: ignore[arg-type]
        status_code=status if status > 0 else None,
        generated_text=generated,
        detail=detail,
    )


def _grammar_for_format(grammar_format: str) -> str:
    if grammar_format == "ll-lark":
        return RegexNode("YES|NO").ll_grammar()
    if grammar_format == "gbnf":
        return FireworksGBNFBuilder().build(RegexNode("YES|NO"))
    if grammar_format == "minimal-lark":
        return 'start: "YES" | "NO"'
    raise ValueError(f"Unsupported grammar format: {grammar_format}")


def _recommended_format(format_counts: dict[str, dict[str, int]]) -> str | None:
    ranked: list[tuple[int, int, str]] = []
    for grammar_format, counts in format_counts.items():
        obey = int(counts.get("accepts+obeys", 0))
        reject = int(counts.get("reject", 0))
        ranked.append((obey, -reject, grammar_format))
    if not ranked:
        return None
    ranked.sort(reverse=True)
    best = ranked[0]
    if best[0] <= 0:
        return None
    return best[2]


def _build_capability_payload(
    *,
    api_base: str,
    models: list[str],
    formats: list[str],
    results: list[ProbeResult],
) -> dict[str, Any]:
    provider_rollup: dict[str, dict[str, Any]] = {}
    model_rollup: dict[str, dict[str, Any]] = {}

    for row in results:
        provider_key = _normalize_provider_name(row.provider)
        model_key = _normalize_model_name(row.model)

        p_entry = provider_rollup.setdefault(
            provider_key,
            {
                "provider_name": row.provider,
                "totals": {"accepts+obeys": 0, "accepts+ignores": 0, "reject": 0},
                "format_outcomes": {},
            },
        )
        p_entry["totals"][row.outcome] += 1
        p_fmt = p_entry["format_outcomes"].setdefault(
            row.grammar_format,
            {"accepts+obeys": 0, "accepts+ignores": 0, "reject": 0},
        )
        p_fmt[row.outcome] += 1

        m_entry = model_rollup.setdefault(
            model_key,
            {
                "model": row.model,
                "providers": {},
            },
        )
        m_provider = m_entry["providers"].setdefault(
            provider_key,
            {
                "provider_name": row.provider,
                "format_outcomes": {},
                "totals": {"accepts+obeys": 0, "accepts+ignores": 0, "reject": 0},
            },
        )
        m_fmt = m_provider["format_outcomes"].setdefault(
            row.grammar_format,
            {"accepts+obeys": 0, "accepts+ignores": 0, "reject": 0},
        )
        m_fmt[row.outcome] += 1
        m_provider["totals"][row.outcome] += 1

    providers_payload: dict[str, Any] = {}
    for provider_key, entry in provider_rollup.items():
        format_outcomes = entry["format_outcomes"]
        recommended = _recommended_format(format_outcomes)
        supports_grammar = int(entry["totals"]["accepts+obeys"]) > 0
        providers_payload[provider_key] = {
            "provider_name": entry["provider_name"],
            "supports_grammar": supports_grammar,
            "recommended_format": recommended,
            "totals": entry["totals"],
            "format_outcomes": format_outcomes,
        }

    models_summary: dict[str, Any] = {}
    for model_key, entry in model_rollup.items():
        provider_payload: dict[str, Any] = {}
        supported_providers: list[str] = []
        for provider_key, provider_entry in entry["providers"].items():
            format_outcomes = provider_entry["format_outcomes"]
            recommended = _recommended_format(format_outcomes)
            supports_grammar = int(provider_entry["totals"]["accepts+obeys"]) > 0
            if supports_grammar:
                supported_providers.append(provider_entry["provider_name"])
            provider_payload[provider_key] = {
                "provider_name": provider_entry["provider_name"],
                "supports_grammar": supports_grammar,
                "recommended_format": recommended,
                "totals": provider_entry["totals"],
                "format_outcomes": format_outcomes,
            }
        models_summary[model_key] = {
            "model": entry["model"],
            "supported_providers": supported_providers,
            "providers": provider_payload,
        }

    return {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "api_base": api_base,
        "models": models,
        "formats": formats,
        "results": [row.__dict__ for row in results],
        "providers": providers_payload,
        "models_summary": models_summary,
    }


def _render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# OpenRouter Provider Grammar Capability Cache",
        "",
        f"- Generated at: `{payload.get('generated_at')}`",
        f"- API base: `{payload.get('api_base')}`",
        f"- Models: `{', '.join(payload.get('models', []))}`",
        f"- Formats: `{', '.join(payload.get('formats', []))}`",
        "",
        "## Provider Summary",
        "",
        "| Provider | Supports Grammar | Recommended Format | Obeys | Ignores | Reject |",
        "|---|---:|---|---:|---:|---:|",
    ]
    providers = payload.get("providers", {})
    if isinstance(providers, dict) and providers:
        for provider_key in sorted(providers):
            row = providers[provider_key]
            totals = row.get("totals", {})
            lines.append(
                f"| {row.get('provider_name', provider_key)} | "
                f"{'yes' if row.get('supports_grammar') else 'no'} | "
                f"{row.get('recommended_format') or ''} | "
                f"{int(totals.get('accepts+obeys', 0))} | "
                f"{int(totals.get('accepts+ignores', 0))} | "
                f"{int(totals.get('reject', 0))} |"
            )
    else:
        lines.append("| (none) | no |  | 0 | 0 | 0 |")

    lines.extend(
        [
            "",
            "## Raw Results",
            "",
            "| Model | Provider | Format | Outcome | HTTP | Generated | Detail |",
            "|---|---|---|---|---:|---|---|",
        ]
    )
    for result in payload.get("results", []):
        if not isinstance(result, dict):
            continue
        generated = str(result.get("generated_text") or "").replace("|", "\\|").replace("\n", "\\n")
        detail = str(result.get("detail") or "").replace("|", "\\|").replace("\n", " ")
        lines.append(
            f"| {result.get('model')} | {result.get('provider')} | {result.get('grammar_format')} | "
            f"{result.get('outcome')} | {result.get('status_code') or ''} | {generated} | {detail} |"
        )
    lines.append("")
    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Discover OpenRouter provider grammar capabilities across models.")
    parser.add_argument(
        "--api-base",
        default=os.getenv("OPENROUTER_BASE_URL", DEFAULT_OPENROUTER_BASE_URL),
        help="OpenRouter API base URL.",
    )
    parser.add_argument(
        "--api-key",
        default=os.getenv("OPENROUTER_API_KEY", os.getenv("OPENAI_API_KEY", "")),
        help="OpenRouter API key.",
    )
    parser.add_argument(
        "--models",
        default=os.getenv("OPENROUTER_FEATURE_TEST_MODELS", os.getenv("OPENROUTER_GRAMMAR_MODEL", "")),
        help="Comma-separated models used to discover provider grammar support.",
    )
    parser.add_argument(
        "--formats",
        default=",".join(DEFAULT_FORMATS),
        help="Comma-separated grammar formats to test. Supported: ll-lark, gbnf, minimal-lark.",
    )
    parser.add_argument(
        "--per-model-provider-limit",
        type=int,
        default=int(os.getenv("OPENROUTER_FEATURE_TEST_PROVIDER_LIMIT", "0")),
        help="Max providers per model (0 = no limit).",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=float,
        default=float(os.getenv("OPENROUTER_FEATURE_TEST_TIMEOUT_SECONDS", "20")),
        help="HTTP timeout per request in seconds.",
    )
    parser.add_argument(
        "--output-json",
        default=str(Path("guidance/resources/openrouter_provider_grammar_capabilities.json")),
        help="Capability cache JSON path.",
    )
    parser.add_argument(
        "--output-markdown",
        default=str(Path("docs/openrouter-provider-grammar-capabilities.md")),
        help="Human-readable markdown summary path.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    api_base = _normalize_api_base(args.api_base)
    api_key = str(args.api_key or "").strip()
    models = _split_csv(args.models)
    formats = _split_csv(args.formats)
    if not formats:
        formats = list(DEFAULT_FORMATS)

    if not api_key:
        print("Missing API key. Set OPENROUTER_API_KEY (or OPENAI_API_KEY).", file=sys.stderr)
        return 2
    if not models:
        print("Missing models. Set OPENROUTER_FEATURE_TEST_MODELS or pass --models.", file=sys.stderr)
        return 2

    for grammar_format in formats:
        _ = _grammar_for_format(grammar_format)

    print(f"API base: {api_base}")
    print(f"Models: {', '.join(models)}")
    print(f"Formats: {', '.join(formats)}")

    results: list[ProbeResult] = []
    for model in models:
        providers = fetch_provider_names(
            api_base=api_base,
            api_key=api_key,
            model=model,
            timeout_seconds=args.timeout_seconds,
        )
        if args.per_model_provider_limit > 0:
            providers = providers[: args.per_model_provider_limit]
        if not providers:
            print(f"{model}: no providers found")
            continue

        print(f"{model}: probing {len(providers)} providers")
        for provider in providers:
            for grammar_format in formats:
                result = probe_provider(
                    api_base=api_base,
                    api_key=api_key,
                    model=model,
                    provider=provider,
                    grammar_format=grammar_format,
                    grammar=_grammar_for_format(grammar_format),
                    timeout_seconds=args.timeout_seconds,
                )
                results.append(result)
                http_code = "" if result.status_code is None else f" ({result.status_code})"
                print(f"  {provider} [{grammar_format}] -> {result.outcome}{http_code}")

    payload = _build_capability_payload(api_base=api_base, models=models, formats=formats, results=results)

    output_json = Path(args.output_json)
    output_markdown = Path(args.output_markdown)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_markdown.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    output_markdown.write_text(_render_markdown(payload), encoding="utf-8")
    print(f"Wrote {output_json}")
    print(f"Wrote {output_markdown}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
