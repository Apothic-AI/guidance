# OpenAI + Fireworks + OpenRouter Grammar Worklog

## Metadata

- Status: current
- Last updated: 2026-02-13
- Audience: contributors implementing provider-native constrained generation

## Scope

This document is a consolidated log of implementation and research for constrained generation across:

- OpenAI native Responses grammar path
- Fireworks native grammar mode (GBNF)
- OpenRouter provider-routed grammar mode, including provider-format probing

Date window covered: Feb 13, 2026 development session(s).

Doc navigation:

- `docs/grammar-integration-docs-index.md`

## Research Links

### OpenAI

- Function calling + grammars:
  - https://developers.openai.com/api/docs/guides/function-calling/
- Noted in docs:
  - Grammar syntax is a Lark variation
  - LLGuidance is used for constrained sampling

### Fireworks

- Structured response formatting overview:
  - https://docs.fireworks.ai/structured-responses/structured-response-formatting.md
- Grammar-based structured outputs (GBNF):
  - https://docs.fireworks.ai/structured-responses/structured-output-grammar-based.md

### OpenRouter

- Models API (`/models`) for metadata catalog:
  - https://openrouter.ai/docs/api/api-reference/models/get-models.md
- Chat completion request schema (`response_format`, including grammar):
  - https://openrouter.ai/docs/api/api-reference/chat/send-chat-completion-request.md
- Structured outputs guide:
  - https://openrouter.ai/docs/guides/features/structured-outputs.md
- Stop conditions doc:
  - https://openrouter.ai/docs/sdks/typescript/call-model/stop-conditions.md
- OpenRouter OpenAPI:
  - https://openrouter.ai/openapi.json

## What Was Implemented

### 1. OpenRouter metadata/capability handling

- Model metadata resolution via `/models` with caching.
- Cache TTL for model catalog set to 1 hour.
- Endpoint metadata (`/models/{model}/endpoints`) used when provider routing is constrained.
- Capability gates for:
  - `tools`
  - `response_format`
  - grammar-specific `response_format` support
  - logprobs/top_logprobs modes
  - modality guards (image/audio)

### 2. OpenRouter stop handling

- Client-side streaming `stop_regex` + `stop_capture` implemented for correctness.
- Literal stop remains provider-side via `stop`.
- This preserves Guidance semantics where provider behavior is insufficient for deterministic earliest-match streaming behavior.

### 3. OpenRouter grammar fast path (fail-closed)

- Added provider grammar request path:
  - `response_format={"type":"grammar","grammar": ...}`
- Local post-validation always required:
  - `node.match(...)` on final text
- Failure behavior is fail-closed:
  - provider rejection -> error
  - unconstrained/non-matching output -> validation error

### 4. OpenAI native grammar path (Responses custom tool)

- Added native OpenAI constrained path using Responses API custom tool grammar:
  - `tools=[{type:"custom", name, format:{type:"grammar", syntax, definition}}]`
  - `tool_choice={"type":"custom","name":"guidance_grammar"}`
- Mapping strategy:
  - regex nodes -> `syntax:"regex"` when possible
  - literal select -> compact regex
  - other supported subset -> conservative Lark adapter
- Local validation and capture propagation are enforced.

### 5. Fireworks grammar path (GBNF adapter)

- Added Fireworks-targeted grammar mode for OpenAI-compatible client path:
  - `response_format={"type":"grammar","grammar":"<gbnf>"}`
- Added conservative Guidance->GBNF adapter subset:
  - literals, alternation, grouping, repetition, char classes, rule refs
- Unsupported constructs raise explicit unsupported-feature errors.
- Local validation remains mandatory.

### 6. Fireworks streaming nuance discovered and patched

- Live behavior observed:
  - for grammar mode on tested Fireworks route/model, streamed generated tokens arrived in `delta.reasoning_content`, not `delta.content`.
- Patch:
  - stream parser now reads `delta.reasoning_content` as generated text for Fireworks base URL clients when `delta.content` is missing.
- This unblocked live constrained success for Fireworks grammar test.

Important note:

- This behavior is unusual enough that we may still be missing nuances of Fireworks streaming semantics.
- Follow-up required: inspect the Fireworks SDK implementation to confirm canonical handling for grammar mode and reasoning-content fields.

### 7. OpenRouter provider-format probing

- Added probe harness:
  - `scripts/openrouter_grammar_probe.py`
- Probes per provider route:
  - LL/Lark grammar
  - GBNF grammar
  - minimal Lark grammar
- Emits matrix artifacts:
- `docs/openrouter-grammar-probe-matrix.md`
- `docs/openrouter-grammar-probe-matrix.json`

### 8. Fireworks SDK investigation + parser/routing tightening (2026-02-14)

SDK inspection findings:

- Fireworks SDK exposes grammar mode as `response_format={"type":"grammar","grammar":"..."}`.
- Fireworks chat message/chunk schema includes both `content` and `reasoning_content`.

Live probes:

- Direct Fireworks grammar streaming (tested model) emitted constrained tokens in `delta.reasoning_content`.
- Direct Fireworks non-stream returned constrained output in `message.content`.
- OpenRouter routed to Fireworks (strict provider settings) emitted constrained stream output in `delta.content`.

Code tightening implemented from those findings:

- Stream parser now supports grammar-mode fallback from `content` to `reasoning_content`:
  - direct Fireworks clients,
  - OpenRouter streams only when chunk provider is Fireworks.
- OpenRouter grammar path now defaults to strict provider routing:
  - `require_parameters=true`,
  - `allow_fallbacks=false`,
  - while preserving explicit user overrides.

Related doc:

- `docs/fireworks-sdk-grammar-investigation.md`

### 9. OpenRouter provider grammar capability cache (2026-02-14)

Implemented new discovery pipeline and shipped runtime cache:

- discovery script:
  - `scripts/openrouter_provider_grammar_discovery.py`
- report output:
  - `docs/openrouter-provider-grammar-capabilities.md`
- shipped cache:
  - `guidance/resources/openrouter_provider_grammar_capabilities.json`

The discovery script consumes model list from:

- `OPENROUTER_FEATURE_TEST_MODELS` (comma-separated)

and probes provider routes using strict provider selection settings from OpenRouter routing docs:

- `provider.order`
- `allow_fallbacks=false`
- `require_parameters=true`

Runtime integration:

- cache-informed provider preference for constrained grammar calls (when no explicit provider route is set),
- cache-informed provider grammar format selection (`ll-lark` vs `gbnf`) when available.

Follow-up correction:

- A raw payload validation pass showed some providers return HTTP 200 with an in-body `error` object.
- Discovery/probe classifiers were updated to treat those responses as `reject`.
- Raw capture artifact:
  - `docs/openrouter-provider-grammar-raw-outputs.json`

## Live Testing Outcomes (So Far)

### Fireworks

- Raw Fireworks grammar call (non-stream) returned constrained output (`YES`) for test grammar.
- Guidance Fireworks constrained test now passes after `reasoning_content` stream handling patch.

### OpenRouter

- Probing still shows substantial provider variance.
- Several routes reject grammar requests at runtime.
- Some routes accept but do not clearly obey constraints.
- Current strategy remains strict fail-closed with local validation.

## Why Fireworks Findings Likely Matter for OpenRouter

- OpenRouter routes to multiple providers, including Fireworks.
- Since Fireworks and OpenRouter routes likely share similar backend constrained-decoding technology paths (LLGuidance-related), request/streaming quirks may overlap.
- Even if not 1:1, adapter and parsing behavior learned from Fireworks is likely close enough to inform OpenRouter integration decisions.

Practical implication:

- The `reasoning_content` streaming nuance should be considered for OpenRouter routes that proxy Fireworks-like streaming payloads.
- Additional route-level stream-payload capture is needed to confirm where this applies.

## Follow-up Actions

1. Investigate Fireworks SDK grammar-mode streaming behavior under the hood and align Guidance parser behavior with official handling.
2. Extend OpenRouter runtime handling if route payloads include `reasoning_content` in place of `content`.
3. Expand OpenRouter provider-format matrix with repeated probes and additional models/providers.
4. Build/maintain a known-good provider/model/format compatibility set for safer automatic serializer selection.
