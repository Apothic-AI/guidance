#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

DEFAULT_MATRIX_PATH = Path("docs/provider-grammar-research-matrix.json")
DEFAULT_OUTPUT_PATH = Path("guidance/resources/openrouter_provider_grammar_policy.json")

# For OpenRouter grammar fast path (`response_format.type="grammar"`), we only treat providers
# with explicit grammar-string support as allowed by policy.
SUPPORTED_FOR_OPENROUTER_GRAMMAR = {
    "grammar_string",
}

# Conservative provider-specific format recommendations for allowed providers.
PROVIDER_FORMAT_HINTS = {
    "fireworks": "gbnf",
}


def _normalized_provider(provider: str) -> str:
    return str(provider).strip().lower()


def _priority_for_row(provider: str, support_level: str) -> int:
    normalized = _normalized_provider(provider)
    if support_level in SUPPORTED_FOR_OPENROUTER_GRAMMAR:
        if normalized == "fireworks":
            return 100
        return 80
    return 0


def _support_reason(support_level: str) -> str:
    if support_level in SUPPORTED_FOR_OPENROUTER_GRAMMAR:
        return "Provider docs indicate explicit grammar-string constrained decoding support."
    return (
        "Provider docs do not indicate OpenRouter-compatible grammar-string constrained decoding "
        "(response_format.type='grammar')."
    )


def _row_to_policy_entry(row: dict[str, Any]) -> tuple[str, dict[str, Any]] | None:
    provider_name = str(row.get("provider", "")).strip()
    support_level = str(row.get("support_level", "")).strip()
    if not provider_name:
        return None
    provider_key = _normalized_provider(provider_name)
    supports = support_level in SUPPORTED_FOR_OPENROUTER_GRAMMAR
    recommended_format = PROVIDER_FORMAT_HINTS.get(provider_key, "ll-lark" if supports else None)
    entry = {
        "provider_name": provider_name,
        "supports_openrouter_grammar_response_format": supports,
        "recommended_grammar_format": recommended_format,
        "priority": _priority_for_row(provider_name, support_level),
        "support_level": support_level,
        "grammar_dialect": str(row.get("grammar_dialect", "")).strip() or None,
        "request_shape_summary": str(row.get("request_shape_summary", "")).strip() or None,
        "streaming_fields_summary": str(row.get("streaming_fields_summary", "")).strip() or None,
        "support_reason": _support_reason(support_level),
        "source_report": str(row.get("source_report", "")).strip() or None,
        "source_urls": row.get("source_urls", []),
    }
    return provider_key, entry


def build_policy(matrix_payload: dict[str, Any], *, matrix_path: str) -> dict[str, Any]:
    rows = matrix_payload.get("rows")
    if not isinstance(rows, list):
        rows = []

    providers: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        converted = _row_to_policy_entry(row)
        if converted is None:
            continue
        key, value = converted
        providers[key] = value

    ranked = sorted(
        (
            value["provider_name"]
            for value in providers.values()
            if bool(value.get("supports_openrouter_grammar_response_format"))
        ),
        key=lambda provider_name: (
            -int(providers[_normalized_provider(provider_name)].get("priority", 0)),
            provider_name.lower(),
        ),
    )

    return {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "matrix_source_path": matrix_path,
        "policy_scope": "openrouter_grammar_response_format",
        "providers": providers,
        "ranked_grammar_providers": ranked,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build OpenRouter provider grammar policy from provider docs matrix.")
    parser.add_argument(
        "--matrix",
        default=str(DEFAULT_MATRIX_PATH),
        help=f"Path to provider docs matrix JSON (default: {DEFAULT_MATRIX_PATH})",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT_PATH),
        help=f"Output policy JSON path (default: {DEFAULT_OUTPUT_PATH})",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    matrix_path = Path(args.matrix)
    output_path = Path(args.output)
    matrix_payload = json.loads(matrix_path.read_text(encoding="utf-8"))

    policy = build_policy(matrix_payload, matrix_path=str(matrix_path))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(policy, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
