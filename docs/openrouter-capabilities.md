# OpenRouter Capability Handling

`guidance` resolves OpenRouter features dynamically from OpenRouter metadata and applies capability-aware request shaping.

## Metadata

- Status: current
- Last updated: 2026-02-13
- Scope: runtime capability detection and request shaping for OpenRouter paths

Related docs:

- `docs/openrouter-grammar-findings.md`
- `docs/openai-fireworks-openrouter-grammar-worklog.md`
- `docs/grammar-integration-docs-index.md`

## Capability Resolution

- Model-level metadata is fetched from `GET /api/v1/models` and cached for 1 hour.
- Endpoint-level metadata (`/models/{model}/endpoints`) is used when provider routing is constrained (for example `provider.order` and/or `require_parameters`).
- Failed metadata lookups are cached briefly (60s) to avoid repeated failures.

## Logprobs and Top-Logprobs

- `guidance` computes an effective mode per request:
  - `disabled`
  - `logprobs_only`
  - `logprobs_and_top_logprobs`
- Unsupported logprob parameters are never sent.
- `top_logprobs` is normalized to a safe bound when supported.
- Stream parsing tolerates OpenAI-compatible schema variants:
  - missing `bytes`
  - missing or null `top_logprobs`
  - mixed dict/object payloads
- For direct Fireworks base URL usage, Guidance also handles streamed generated text arriving as
  `delta.reasoning_content` when `delta.content` is empty.
  - This was observed in grammar mode for tested Fireworks routes/models.
  - We should verify whether OpenRouter Fireworks-backed routes require the same handling.

## Capture Log Probability

- For OpenAI/OpenRouter rule captures, `guidance` aggregates token logprobs for the exact captured span.
- Capture logprob is the sum of token logprobs when every captured token has a usable probability.
- If token probabilities are missing or token/text alignment is partial, capture logprob is `None`.

## OpenRouter `stop_regex` and `stop_capture`

- OpenRouter now supports client-side `stop_regex` matching in streaming rule generation.
- When a regex stop match is found:
  - emitted text excludes the matched stop text
  - optional `stop_capture` is populated with the matched stop text
  - capture variables store only emitted text (not stop text or overrun)
- If no match occurs before stream end:
  - all generated text is emitted
  - `stop_capture` remains unset

## OpenRouter Grammar Fast Path

- `guidance` now attempts provider-side grammar-constrained decoding for OpenRouter grammar/regex nodes via:
  - `response_format={"type":"grammar","grammar": "<serialized_grammar>"}`.
- Serializer selection is provider-aware:
  - default: Guidance LL/Lark,
  - initial provider hint: `Fireworks -> GBNF`.
- This path is gated on OpenRouter metadata indicating `response_format` support for the current provider routing.
- Output is validated locally against the original `guidance` grammar after generation:
  - provider rejection raises a grammar-specific error,
  - unconstrained/mismatched output raises validation error.
- This is intentionally fail-closed, since provider support quality varies in practice.

Probe harness for provider/format behavior:

- `scripts/openrouter_grammar_probe.py`
- writes matrix artifacts under `docs/openrouter-grammar-probe-matrix.*`
- See full consolidated worklog:
  - `docs/openai-fireworks-openrouter-grammar-worklog.md`

## Current Limits

- `suffix` remains unsupported for OpenRouter rule generation.
- `stop_capture` for OpenRouter is currently supported with `stop_regex` paths (not literal provider-side `stop`).

## Credentialed Test Runs

Load local `.env` automatically using `dotenv`:

```bash
dotenv python -m pytest -q tests/need_credentials/test_openrouter.py
```

OpenRouter credentialed tests accept:

- `OPENROUTER_API_KEY` (preferred), or
- `OPENAI_API_KEY` when `OPENAI_BASE_URL`/`OPENROUTER_BASE_URL` points at OpenRouter.
