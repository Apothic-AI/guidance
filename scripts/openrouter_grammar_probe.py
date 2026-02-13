#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib import error as urllib_error
from urllib import parse as urllib_parse
from urllib import request as urllib_request

from guidance._ast import RegexNode
from guidance.models._grammar_support import FireworksGBNFBuilder

DEFAULT_OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


@dataclass
class ProbeResult:
    provider: str
    grammar_format: str
    outcome: str
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
        key = provider.lower()
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


def probe_provider(
    *,
    api_base: str,
    api_key: str,
    model: str,
    provider: str,
    grammar: str,
    grammar_format: str,
    timeout_seconds: float,
) -> ProbeResult:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are concise."},
            {"role": "user", "content": "Reply using exactly one token: MAYBE"},
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
    generated = _extract_content_text(parsed)
    outcome, detail = _classify_outcome(status, generated)
    if outcome == "reject":
        reason = ""
        if isinstance(parsed, dict):
            message = parsed.get("error")
            if isinstance(message, dict):
                msg_text = message.get("message")
                if isinstance(msg_text, str):
                    reason = msg_text
            elif isinstance(message, str):
                reason = message
        if not reason:
            reason = raw_text[:240].replace("\n", " ")
        detail = f"{detail}: {reason}"
    return ProbeResult(
        provider=provider,
        grammar_format=grammar_format,
        outcome=outcome,
        status_code=status if status > 0 else None,
        generated_text=generated,
        detail=detail,
    )


def _render_markdown(*, model: str, api_base: str, results: list[ProbeResult]) -> str:
    generated_at = datetime.now(UTC).isoformat()
    lines = [
        "# OpenRouter Grammar Probe Matrix",
        "",
        f"- Generated at: `{generated_at}`",
        f"- API base: `{api_base}`",
        f"- Model: `{model}`",
        "",
        "| Provider | Format | Outcome | HTTP | Generated | Detail |",
        "|---|---|---|---:|---|---|",
    ]
    for row in results:
        generated = (row.generated_text or "").replace("|", "\\|").replace("\n", "\\n")
        detail = row.detail.replace("|", "\\|").replace("\n", " ")
        http_code = "" if row.status_code is None else str(row.status_code)
        lines.append(f"| {row.provider} | {row.grammar_format} | {row.outcome} | {http_code} | {generated} | {detail} |")
    if not results:
        lines.append("| (none) | (none) | (none) |  |  | no probe results |")
    lines.append("")
    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Probe OpenRouter provider grammar behavior across grammar formats.")
    parser.add_argument(
        "--api-base",
        default=os.getenv("OPENROUTER_BASE_URL", DEFAULT_OPENROUTER_BASE_URL),
        help="OpenRouter API base URL (default: OPENROUTER_BASE_URL or https://openrouter.ai/api/v1)",
    )
    parser.add_argument(
        "--api-key",
        default=os.getenv("OPENROUTER_API_KEY", os.getenv("OPENAI_API_KEY", "")),
        help="OpenRouter API key (default: OPENROUTER_API_KEY or OPENAI_API_KEY)",
    )
    parser.add_argument(
        "--model",
        default=os.getenv("OPENROUTER_GRAMMAR_PROBE_MODEL", os.getenv("OPENROUTER_GRAMMAR_MODEL", "")),
        help="Model ID to probe (default: OPENROUTER_GRAMMAR_PROBE_MODEL or OPENROUTER_GRAMMAR_MODEL)",
    )
    parser.add_argument(
        "--providers",
        default=os.getenv("OPENROUTER_GRAMMAR_PROBE_PROVIDERS", ""),
        help="Comma-separated provider list. If omitted, providers are fetched from /models/{id}/endpoints.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=int(os.getenv("OPENROUTER_GRAMMAR_PROBE_LIMIT", "6")),
        help="Maximum number of providers to probe when auto-discovering providers.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=float,
        default=float(os.getenv("OPENROUTER_GRAMMAR_PROBE_TIMEOUT_SECONDS", "20")),
        help="HTTP timeout per request in seconds.",
    )
    parser.add_argument(
        "--output-markdown",
        default=str(Path("docs") / "openrouter-grammar-probe-matrix.md"),
        help="Path to write markdown matrix output.",
    )
    parser.add_argument(
        "--output-json",
        default=str(Path("docs") / "openrouter-grammar-probe-matrix.json"),
        help="Path to write JSON matrix output.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    api_base = _normalize_api_base(args.api_base)
    api_key = str(args.api_key or "").strip()
    model = str(args.model or "").strip()
    if not api_key:
        print("Missing API key. Set OPENROUTER_API_KEY or pass --api-key.", file=sys.stderr)
        return 2
    if not model:
        print("Missing model. Set OPENROUTER_GRAMMAR_PROBE_MODEL or pass --model.", file=sys.stderr)
        return 2

    if args.providers:
        providers = [item.strip() for item in str(args.providers).split(",") if item.strip()]
    else:
        providers = fetch_provider_names(
            api_base=api_base,
            api_key=api_key,
            model=model,
            timeout_seconds=args.timeout_seconds,
        )
    if args.limit > 0:
        providers = providers[: args.limit]
    if not providers:
        print("No providers found to probe.", file=sys.stderr)
        return 3

    ll_lark = RegexNode("YES|NO").ll_grammar()
    gbnf = FireworksGBNFBuilder().build(RegexNode("YES|NO"))
    minimal_lark = 'start: "YES" | "NO"'
    grammars = [
        ("ll-lark", ll_lark),
        ("gbnf", gbnf),
        ("minimal-lark", minimal_lark),
    ]

    results: list[ProbeResult] = []
    for provider in providers:
        for format_name, grammar in grammars:
            result = probe_provider(
                api_base=api_base,
                api_key=api_key,
                model=model,
                provider=provider,
                grammar=grammar,
                grammar_format=format_name,
                timeout_seconds=args.timeout_seconds,
            )
            results.append(result)
            http_code = "" if result.status_code is None else f" ({result.status_code})"
            print(f"{provider} [{format_name}] -> {result.outcome}{http_code}")

    markdown_path = Path(args.output_markdown)
    json_path = Path(args.output_json)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.write_text(_render_markdown(model=model, api_base=api_base, results=results), encoding="utf-8")
    json_path.write_text(
        json.dumps(
            {
                "generated_at": datetime.now(UTC).isoformat(),
                "api_base": api_base,
                "model": model,
                "results": [result.__dict__ for result in results],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {markdown_path}")
    print(f"Wrote {json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
