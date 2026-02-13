# OpenAI + Fireworks Native Grammar Path Plan

## Metadata

- Status: mixed (current implementation status + historical plan)
- Last updated: 2026-02-13
- Canonical companion docs:
  - `docs/openai-fireworks-openrouter-grammar-worklog.md`
  - `docs/grammar-integration-docs-index.md`

## Document Role

This document contains:

- implementation status notes (current),
- the original plan text (retained for traceability).

For the consolidated up-to-date narrative, see:

- `docs/openai-fireworks-openrouter-grammar-worklog.md`
- `docs/grammar-integration-docs-index.md`

## Implementation Status (2026-02-13)

Comprehensive implementation/research log:

- `docs/openai-fireworks-openrouter-grammar-worklog.md`

Implemented in this branch:

- OpenAI native grammar path is implemented via Responses custom tools:
  - `tools=[{type:"custom", format:{type:"grammar", syntax, definition}}]`
  - `tool_choice={"type":"custom","name":"guidance_grammar"}`
  - supported syntax selection:
    - `regex` for `RegexNode` and literal-only selects,
    - `lark` for a conservative Guidance subset via adapter.
- Fireworks grammar path is implemented for OpenAI-compatible clients targeting Fireworks:
  - `response_format={"type":"grammar","grammar":"<gbnf>"}`.
  - grammar string is produced by a new conservative GBNF adapter.
  - stream handling includes a Fireworks-specific fallback for grammar mode where tokens may arrive in
    `delta.reasoning_content` instead of `delta.content`.
- Shared fail-closed validation is implemented:
  - standardized constraint errors,
  - local `node.match(...)` validation for all native paths,
  - capture propagation into Guidance state.
- OpenRouter GBNF investigation tooling is implemented:
  - probe harness script: `scripts/openrouter_grammar_probe.py`,
  - matrix artifacts:
    - `docs/openrouter-grammar-probe-matrix.md`,
    - `docs/openrouter-grammar-probe-matrix.json`.
- OpenRouter runtime strategy has initial provider-aware selection:
  - provider hint `Fireworks -> gbnf`,
  - default remains `ll-lark`,
  - fail-closed local validation remains mandatory.

Implemented tests:

- Unit:
  - `tests/unit/test_openai_provider_grammar.py`
  - updated `tests/unit/test_openrouter_grammar.py`
  - updated `tests/unit/test_openrouter_capabilities.py`
- Need-credentials:
  - `tests/need_credentials/test_openai_fireworks_grammar.py`
  - `tests/need_credentials/test_openrouter_grammar_probe.py` (gated by `OPENROUTER_ENABLE_GRAMMAR_PROBE_TEST=1`).

Executed test commands:

```bash
python -m pytest -q tests/unit/test_openai_provider_grammar.py tests/unit/test_openrouter_grammar.py tests/unit/test_openrouter_streaming.py tests/unit/test_openrouter_capabilities.py tests/unit/test_model.py tests/unit/test_grammar.py tests/unit/test_parser.py
dotenv python -m pytest -q -rs tests/need_credentials/test_openrouter.py tests/need_credentials/test_openai_fireworks_grammar.py tests/need_credentials/test_openrouter_grammar_probe.py
dotenv python scripts/openrouter_grammar_probe.py --model "${OPENROUTER_GRAMMAR_PROBE_MODEL:-z-ai/glm-5}" --limit 6 --output-markdown docs/openrouter-grammar-probe-matrix.md --output-json docs/openrouter-grammar-probe-matrix.json
```

Credentialed test note:

- OpenAI and Fireworks grammar tests are present but skipped unless `OPENAI_GRAMMAR_MODEL` and `FIREWORKS_GRAMMAR_MODEL` are set.
- Fireworks constrained generation is live-tested as passing after the `reasoning_content` stream parsing fix.
  - Most recent confirmed passing live run used:
    - model: `accounts/fireworks/models/glm-5`
    - test: `tests/need_credentials/test_openai_fireworks_grammar.py::test_fireworks_native_grammar_regex_success`

Important follow-up note:

- It is still somewhat odd that grammar-mode output streamed via `delta.reasoning_content` on tested Fireworks routes.
- We should inspect the Fireworks SDK behavior for grammar mode to confirm canonical field handling and avoid relying on accidental behavior.
- The same nuance may apply to OpenRouter routes backed by Fireworks-like providers.

## Original Plan (Historical Baseline)

Implement first-class constrained-generation support for:

1. OpenAI native grammar path via Responses custom-tool grammar.
2. Fireworks grammar mode via `response_format.type="grammar"` with a GBNF adapter.

Keep Guidance guarantees by validating outputs locally and failing closed when provider behavior diverges.

## Why This Plan
- Guidance's core value includes hard output constraints (`regex`, `select`, CFG-like structure).
- OpenAI and Fireworks both expose native grammar-constraining APIs, but with different request shapes and grammar dialect expectations.
- Current OpenRouter results indicate provider variance; correctness must not depend on provider claims alone.

## Deliverable A: OpenAI Native Grammar (Responses API)

### A1. Provider Path
- Add a dedicated OpenAI Responses client path for grammar constraints (do not tunnel through chat completions for this feature).
- Trigger path only for constraint nodes where mapping is supported (`RegexNode`, `SelectNode`, `GrammarNode` subset).

### A2. Grammar Request Shape
- Use Responses custom tool grammar format:
  - `tools: [{type: "custom", name, format: {type: "grammar", syntax, definition}}]`
- Start with explicit `syntax` selection:
  - `lark` where Guidance grammar can be translated safely.
  - `regex` for pure regex constraints when cleaner.

### A3. Node Mapping
- `RegexNode(pattern)` -> `syntax: "regex"` when compatible.
- `SelectNode([...])` -> compact grammar with exact literals.
- `GrammarNode` -> conservative subset to Lark, with fallback if unsupported features are detected.

### A4. Safety + Semantics
- Always run local `node.match(...)` post-validation on returned text.
- If validation fails, raise explicit constraint failure (fail closed).
- Preserve capture behavior by applying match captures to Guidance state.

### A5. Compatibility Guardrails
- If grammar complexity or unsupported syntax is detected, raise a targeted error or fall back to existing unconstrained path only when explicitly allowed by config.
- Keep default behavior strict for constraint requests.

## Deliverable B: Fireworks Grammar Mode + GBNF Adapter

### B1. Provider Path
- Add Fireworks-specific grammar path (OpenAI-compatible client, provider-specific request shaping).
- Use `response_format: {"type":"grammar", "grammar": "..."}`.

### B2. GBNF Adapter
- Introduce adapter module to convert Guidance grammar subset -> GBNF.
- Initial supported subset:
  - literals, alternation, grouping, repetition, char classes, rule refs.
- Explicitly reject unsupported constructs with actionable errors.

### B3. Regex Handling
- Prefer direct regex rendering where compatible with Fireworks/GBNF expectations.
- Detect and reject known incompatible constructs (e.g., lookarounds/lazy modifiers if unsupported).

### B4. Safety + Semantics
- Keep local post-validation and capture extraction identical to OpenAI plan.
- Fail closed on provider drift.

## Deliverable C: OpenRouter GBNF Investigation Track

## Hypothesis
OpenRouter grammar support may pass through to providers that expect GBNF-like grammar in some routes.

### C1. Experiments
- Add probe harness to test, per provider route:
  - Guidance LL grammar string.
  - GBNF grammar string.
  - Minimal lark-style grammar.
- Compare acceptance rate and constraint obedience for each format.

### C2. Output Criteria
- Build provider-format compatibility matrix:
  - `provider x {ll-lark, gbnf, minimal-lark}` -> {reject, accepts+obeys, accepts+ignores}.
- Use matrix to select grammar serializer per OpenRouter provider.

### C3. Runtime Strategy
- Route-specific grammar serializer selection where signal is reliable.
- If unknown route behavior, keep fail-closed validation and surface clear errors.

## Cross-Cutting Architecture

### Shared Components
- `GrammarRequestBuilder` abstraction with provider backends:
  - OpenAIResponsesGrammarBuilder
  - FireworksGBNFBuilder
  - OpenRouterProviderAwareBuilder (future extension)
- Shared `ConstraintValidation` utility:
  - local `match` check
  - standardized error types
  - capture application

### Error Model
- `ConstraintProviderRejectedError`
- `ConstraintValidationFailedError`
- `ConstraintUnsupportedFeatureError`

## Testing Plan

### Unit Tests
- Grammar mapping serialization tests for each backend.
- Unsupported syntax detection tests.
- Local validation + capture application tests.

### Need-Credentials Tests
- OpenAI: at least one model/provider showing true constrained success with native grammar path.
- Fireworks: at least one model showing constrained success with GBNF adapter.
- OpenRouter: probe tests that produce compatibility matrix artifacts.

### Regression Tests
- Existing OpenRouter stop/logprobs behavior unchanged.
- Existing engine-backed grammar behavior unchanged.

## Rollout Phases

1. OpenAI Responses grammar path (strict subset + validation).
2. Fireworks GBNF adapter + native path.
3. OpenRouter provider-format probes and optional provider-aware serializer selection.
4. Docs + capability matrix publication.

## Success Criteria
- Guidance constraints (`regex`, `select`, subset CFG) have native-path success on OpenAI and Fireworks.
- No silent unconstrained success: all mismatches are caught by local validation.
- Clear provider-specific errors for unsupported or drifting behavior.
