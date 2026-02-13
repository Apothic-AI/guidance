# OpenRouter Grammar Findings (Current)

This document records what we have verified about OpenRouter grammar support, and how it maps to `guidance` semantics.

## Metadata

- Status: current
- Last updated: 2026-02-13
- Scope: OpenRouter grammar behavior, probe outcomes, and follow-up risks

Related docs:

- `docs/openrouter-capabilities.md`
- `docs/openai-fireworks-openrouter-grammar-worklog.md`
- `docs/grammar-integration-docs-index.md`

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
- https://openrouter.ai/docs/guides/features/structured-outputs.md
- https://docs.fireworks.ai/structured-responses/structured-response-formatting.md
- https://docs.fireworks.ai/structured-responses/structured-output-grammar-based.md

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
  - send `response_format={"type":"grammar","grammar": ...}`
  - serializer is provider-aware:
    - default: Guidance LL/Lark (`node.ll_grammar()`),
    - provider hint `Fireworks`: GBNF adapter output.
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

## Probe Matrix (ll-lark vs gbnf vs minimal-lark)

A probe harness was added and executed against `z-ai/glm-5`:

- Script: `scripts/openrouter_grammar_probe.py`
- Artifacts:
  - `docs/openrouter-grammar-probe-matrix.md`
  - `docs/openrouter-grammar-probe-matrix.json`

Observed sample outcomes (Feb 13, 2026):

- `AtlasCloud`: `ll-lark` accepted but did not obey constraints (empty/non-text output), `gbnf`/`minimal-lark` rejected due provider errors/rate limits.
- `Friendli`, `GMICloud`, `Venice`: all three formats rejected.
- `Parasail`: all tested formats rejected/rate-limited.
- `Novita`: all tested formats rejected (502 provider errors).

This confirms that format choice alone does not guarantee constrained behavior across routes.

## Fireworks Streaming Nuance (Potentially Relevant to OpenRouter)

In live Fireworks grammar-mode testing (direct Fireworks endpoint), generated text streamed in
`delta.reasoning_content` rather than `delta.content` for the tested route/model.

Why this matters for OpenRouter:

- OpenRouter can route to Fireworks and other providers that may share backend constrained-decoding internals.
- If OpenRouter forwards similar payload structure for some routes, content extraction may require parallel handling.

Current status:

- Guidance now handles this field for direct Fireworks endpoints.
- OpenRouter route-specific behavior still needs deeper payload-level validation.

Follow-up:

- inspect Fireworks SDK grammar-mode stream handling to confirm canonical semantics.
- compare OpenRouter streamed payloads on Fireworks-backed routes to decide if equivalent parsing should be generalized.

## Remaining Work

1. Expand provider-aware serializer hints beyond the initial `Fireworks -> gbnf` mapping using repeated probe data.
2. Maintain a known-good model/provider/format matrix and use it for safer auto-routing defaults.
3. Add adaptive retries/fallback policy (while staying fail-closed) for transient provider errors (429/5xx).
4. Validate whether OpenRouter Fireworks-backed streams expose text via `reasoning_content` and update parser logic if needed.

## Test Environment Notes

Credentialed OpenRouter tests now accept either:

- `OPENROUTER_API_KEY` (preferred), or
- `OPENAI_API_KEY` when `OPENAI_BASE_URL`/`OPENROUTER_BASE_URL` points to OpenRouter.

To ensure local `.env` is loaded for test runs:

```bash
dotenv python -m pytest -q tests/need_credentials/test_openrouter.py
```
