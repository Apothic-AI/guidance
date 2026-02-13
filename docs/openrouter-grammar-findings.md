# OpenRouter Grammar Findings (Current)

This document records what we have verified about OpenRouter grammar support, and how it maps to `guidance` semantics.

## Verified API Surface

From OpenRouter API docs and OpenAPI schema:

- Chat request `response_format` supports:
  - `{"type":"text"}`
  - `{"type":"json_object"}`
  - `{"type":"json_schema", "json_schema": ...}`
  - `{"type":"grammar", "grammar":"..."}`
  - `{"type":"python"}`
- The grammar object is currently represented as `ResponseFormatTextGrammar` with required fields:
  - `type` (const `grammar`)
  - `grammar` (string)

References:

- https://openrouter.ai/docs/api/api-reference/chat/send-chat-completion-request.md
- https://openrouter.ai/openapi.json

## Important Observations

OpenRouter exposes a provider-facing grammar-constrained output mode, but it is distinct from `guidance` `gen(stop_regex=..., save_stop_text=...)` runtime semantics.

`guidance` `stop_regex` semantics require:

- incremental streaming detection
- deterministic earliest-match behavior
- omission of matched stop text from emitted output
- optional `stop_capture` assignment to the matched stop text

These are streaming control semantics, not just output-shape constraints.

## Why Grammar Is Not a Drop-In for `stop_regex`

Using provider grammar directly for `stop_regex`/`stop_capture` is non-trivial:

- Grammar mode constrains generated output; it does not directly provide "first stop match" eventing.
- `stop_capture` needs exact extraction of the matched stop span.
- Earliest-match enforcement (including boundary behavior during stream) is hard to guarantee from grammar output alone.
- OpenRouter docs currently expose `grammar` as a raw string with limited dialect-specific detail and provider caveats.

Because of this, client-side streaming enforcement remains the correctness-first implementation for `stop_regex` and `stop_capture`.

## Implemented in Guidance

- We keep client-side `stop_regex` + `stop_capture` for OpenRouter.
- We preserve provider-side literal `stop` behavior for literal stops.
- We added an OpenRouter provider-grammar fast path for grammar/regex nodes:
  - send `response_format={"type":"grammar","grammar": node.ll_grammar()}`
  - only when provider routing reports `response_format` support
  - validate returned text locally with `node.match(...)`
- We fail closed:
  - if provider rejects grammar requests, raise a grammar-specific `ValueError`
  - if provider returns text that does not satisfy the grammar, raise a validation `ValueError`

## Runtime Variability (Observed)

Provider behavior is not uniform even when endpoint metadata advertises `response_format` support:

- Some providers appear to ignore grammar constraints for `response_format.type="grammar"` and return unconstrained text.
- Some providers reject grammar requests at runtime.
- Because of this, local post-generation grammar validation is required to preserve correctness guarantees.

## Remaining Work

1. Expand provider-aware grammar capability detection beyond `response_format` metadata.
2. Add stronger provider-specific compatibility tests and a known-good model/provider matrix.
3. Add targeted optimizations for the supported Lark/regex subset used by OpenRouter providers.

## Test Environment Notes

Credentialed OpenRouter tests now accept either:

- `OPENROUTER_API_KEY` (preferred), or
- `OPENAI_API_KEY` when `OPENAI_BASE_URL`/`OPENROUTER_BASE_URL` points to OpenRouter.

To ensure local `.env` is loaded for test runs:

```bash
dotenv python -m pytest -q tests/need_credentials/test_openrouter.py
```
