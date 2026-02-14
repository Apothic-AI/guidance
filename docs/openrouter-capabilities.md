# OpenRouter Capability Handling

`guidance` resolves OpenRouter features dynamically from OpenRouter metadata and applies capability-aware request shaping.

## Metadata

- Status: current
- Last updated: 2026-02-14
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
- Constrained grammar calls now default to stricter provider routing:
  - `extra_body.provider.require_parameters=true`
  - `extra_body.provider.allow_fallbacks=false`
  - explicit user-provided routing settings are preserved.
- Serializer selection is provider-aware:
  - default: Guidance LL/Lark,
  - initial provider hint: `Fireworks -> GBNF`.
- Provider grammar capability cache:
  - shipped file: `guidance/resources/openrouter_provider_grammar_capabilities.json`
  - shipped provider policy overlay: `guidance/resources/openrouter_provider_grammar_policy.json`
  - generated/updated via discovery script:
    - `scripts/openrouter_provider_grammar_discovery.py`
  - policy build script (from provider-doc matrix):
    - `scripts/build_openrouter_provider_grammar_policy.py`
  - when cache has model-supported providers, constrained OpenRouter grammar calls now prefer those providers.
  - when model-specific cache data is missing, constrained grammar calls fall back to ranked providers from the
    shipped policy.
  - ranked fallback providers are intersected with the model's available OpenRouter endpoints before setting
    `provider.order`, to avoid forcing unavailable providers.
  - cache also contributes provider-specific format hints (`ll-lark` vs `gbnf`) when available.
  - policy entries provide a hard denylist for providers documented as not supporting
    `response_format.type="grammar"` on OpenRouter.
- This path is gated on OpenRouter metadata indicating `response_format` support for the current provider routing.
- Output is validated locally against the original `guidance` grammar after generation:
  - provider rejection raises a grammar-specific error,
  - unconstrained/mismatched output raises validation error.
- This is intentionally fail-closed, since provider support quality varies in practice.
- Stream parsing supports a grammar-mode `reasoning_content` fallback for OpenRouter only when chunk provider is
  Fireworks, based on live provider behavior variance.

Probe harness for provider/format behavior:

- `scripts/openrouter_grammar_probe.py`
- writes matrix artifacts under `docs/openrouter-grammar-probe-matrix.*`
- capability discovery + cache generation:
  - `scripts/openrouter_provider_grammar_discovery.py`
  - writes:
    - `docs/openrouter-provider-grammar-capabilities.md`
    - `guidance/resources/openrouter_provider_grammar_capabilities.json`
- See full consolidated worklog:
  - `docs/openai-fireworks-openrouter-grammar-worklog.md`

Refresh capability cache from `.env` model list:

```bash
dotenv python scripts/openrouter_provider_grammar_discovery.py \
  --models "${OPENROUTER_FEATURE_TEST_MODELS}" \
  --formats ll-lark,gbnf \
  --output-json guidance/resources/openrouter_provider_grammar_capabilities.json \
  --output-markdown docs/openrouter-provider-grammar-capabilities.md

python scripts/build_openrouter_provider_grammar_policy.py \
  --matrix docs/provider-grammar-research-matrix.json \
  --output guidance/resources/openrouter_provider_grammar_policy.json
```

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
