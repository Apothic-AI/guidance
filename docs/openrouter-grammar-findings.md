# OpenRouter Grammar Findings (Current)

This document records what we have verified so far about OpenRouter grammar support, and how it relates to `guidance` semantics.

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

## Important Observation

OpenRouter exposes a provider-facing grammar-constrained output mode, but it is distinct from `guidance` `gen(stop_regex=..., save_stop_text=...)` runtime semantics.

`guidance` `stop_regex` semantics require:

- incremental streaming detection
- deterministic earliest-match behavior
- omission of matched stop text from emitted output
- optional `stop_capture` assignment to the matched stop text

These are streaming control semantics, not just output-shape constraints.

## Why Grammar Mode Is Not Yet a Drop-In for `stop_regex`

Using provider grammar directly for `stop_regex`/`stop_capture` is non-trivial:

- Grammar mode constrains generated output; it does not directly provide "first stop match" eventing.
- `stop_capture` needs exact extraction of the matched stop span.
- Earliest-match enforcement (including boundary behavior during stream) is hard to guarantee from grammar output alone.
- OpenRouter docs currently expose `grammar` as a raw string with limited dialect-specific detail and provider caveats.

Because of this, client-side streaming enforcement remains the correctness-first implementation for `stop_regex` and `stop_capture`.

## Current Guidance Position

- We keep client-side `stop_regex` + `stop_capture` for OpenRouter today.
- We preserve provider-side literal `stop` behavior for literal stops.
- We continue capability-gated request shaping (for example `logprobs`, `top_logprobs`, `tools`, `response_format`).

## Candidate Fast-Path Strategy (Future)

A provider-grammar fast path is still possible, but should be phased:

1. Gate by explicit capability and provider routing conditions.
2. Start with strict subsets where semantics are easier to prove.
3. Keep client-side matcher as fallback and as semantic source of truth.
4. Add integration parity tests comparing fast-path vs client-side behavior.

## Test Environment Notes

Credentialed OpenRouter tests now accept either:

- `OPENROUTER_API_KEY` (preferred), or
- `OPENAI_API_KEY` when `OPENAI_BASE_URL`/`OPENROUTER_BASE_URL` points to OpenRouter.

To ensure local `.env` is loaded for test runs:

```bash
dotenv python -m pytest -q tests/need_credentials/test_openrouter.py
```
