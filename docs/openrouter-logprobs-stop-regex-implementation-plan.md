# OpenRouter: Logprobs + Client-Side `stop_regex`/`stop_capture` Implementation Plan

## Scope
This plan covers two deliverables for OpenRouter-backed models in `guidance`:

1. Fully utilize logprobs/top-logprobs when the selected OpenRouter model/provider supports them.
2. Implement client-side streaming support for `stop_regex` and `stop_capture` in OpenRouter paths.

The goal is to maximize model capabilities without adding per-request metadata fetches.

## Current Baseline
- OpenRouter model metadata is now cached via `/api/v1/models`, with endpoint fallback for provider-constrained routing.
- Request-time gating already disables unsupported parameters (for example logprobs/top_logprobs).
- OpenRouter rule path currently supports literal `stop`, but not `stop_regex` or `stop_capture`.
- Capture log probability in OpenAI/OpenRouter rule paths is currently a placeholder (`log_prob=1`).

## Deliverable A: Full Logprobs Utilization

### A1. Capability Resolution Policy
- Keep current metadata-first capability decision:
  - Use model catalog (`supported_parameters`) when provider is unconstrained.
  - Use provider-filtered endpoint metadata when `provider.order` and/or `require_parameters` is set.
- Add explicit helper for effective logprobs mode:
  - `disabled`, `logprobs_only`, `logprobs_and_top_logprobs`.

### A2. Request Contract
- Ensure request construction is explicit and consistent:
  - Send `logprobs=True` only when supported.
  - Send `top_logprobs=<k>` only when supported.
  - Never send unsupported fields.
- Add guardrails for `top_logprobs` value:
  - Clamp or validate against safe bounds if provider-specific limits are unknown.

### A3. Stream Parsing Robustness
- Harden `_handle_stream` logprobs parsing:
  - Tolerate missing `bytes`, missing `top_logprobs`, partial chunks, or provider-specific shape differences.
  - Keep fallback to `TextOutput` when logprobs content is absent.
- Add compatibility shim function for extracting token probability payloads from chunk variants.

### A4. Capture-Level Log Probability
- Replace placeholder capture log prob in OpenAI/OpenRouter rule mixins:
  - Aggregate token-level logprobs for captured text when available.
  - Define deterministic behavior when tokens/segments are mixed:
    - Sum token log-probabilities for the captured span.
    - Return `None` if per-token probabilities are not available for all captured tokens.
- Ensure `lm.log_prob(name)` reflects real values for OpenRouter-compatible runs.

### A5. Tests for Deliverable A
- Unit tests:
  - Capability mode resolution across model metadata and provider-constrained endpoint metadata.
  - Request kwargs inclusion/exclusion for `logprobs` and `top_logprobs`.
  - Parser behavior for chunk variants (with/without top logprobs, with null fields).
  - Capture log-prob aggregation correctness.
- Need-credentials integration tests (OpenRouter):
  - Positive: a model/provider combination with logprobs support emits `TokenOutput` with probabilities.
  - Negative: unsupported model/provider automatically falls back without API errors.

### A6. Acceptance Criteria for Deliverable A
- No unsupported logprob fields are sent to OpenRouter.
- Token-level probabilities are emitted whenever model/provider supports them.
- Capture-level `log_prob` is no longer a placeholder where data is available.
- Behavior is stable under constrained routing and unconstrained routing.

## Deliverable B: Client-Side `stop_regex` + `stop_capture` for OpenRouter Streaming

### B1. Design Approach
- Implement a streaming stop matcher in `OpenRouterRuleMixin.rule`:
  - Continue requesting streamed text from OpenRouter.
  - Maintain a rolling output buffer and detect earliest regex match incrementally.
  - On match:
    - Exclude matched stop text from captured generation output.
    - Optionally store matched stop text into `stop_capture`.
    - Terminate local emission and stop consuming further chunks.
- Keep provider API `stop` behavior for literal stops unchanged.

### B2. Matching Engine
- Use Python `re` with compiled pattern from `RegexNode`.
- Maintain two buffers:
  - `raw_generated`: everything received from stream.
  - `emitted_generated`: text already yielded to caller.
- To avoid broken chunk boundaries:
  - Match against `raw_generated` each step.
  - Compute a safe emit boundary (content proven not part of a future earliest match).
- Define deterministic first-match behavior:
  - Use earliest start index.
  - If ties, prefer earliest end index.

### B3. Emission + State Semantics
- When no match:
  - Emit incremental text normally.
- When match occurs:
  - Emit only text before match start.
  - Do not emit stop-match text.
  - Save capture variable for `node.capture` from emitted text only.
  - Save stop text to `node.stop_capture` when requested.
  - End rule execution cleanly without extra generated text.
- Ensure model state (`self.state.apply_text`) stays consistent with emitted text, not raw stream overrun.

### B4. Interaction with Existing Features
- Compatible with:
  - `temperature`, `max_tokens`.
  - List append captures.
  - OpenRouter sampling parameter filtering.
- Explicit non-goals for first pass:
  - Regex lookbehind optimizations for pathological patterns.
  - Multi-alternative streaming automata beyond Python `re`.

### B5. Error Handling
- Invalid regex should raise early with clear `ValueError`.
- If stream closes before a match:
  - Emit all generated text.
  - `stop_capture` remains unset.
- If API returns tool calls or non-text deltas in this rule context:
  - Keep current behavior, but document unsupported mixes.

### B6. Tests for Deliverable B
- Unit tests for `OpenRouterRuleMixin.rule` with mocked chunk streams:
  - Match wholly inside one chunk.
  - Match spanning chunk boundary.
  - Multiple possible matches where earliest should win.
  - No match path.
  - `stop_capture=True` and custom stop-capture key.
  - `list_append=True` capture behavior.
- Regression tests:
  - Existing literal `stop` behavior unchanged.
  - `suffix` and unsupported features continue to raise expected errors.

### B7. Acceptance Criteria for Deliverable B
- `gen(stop_regex=...)` works with OpenRouter models via client-side enforcement.
- `save_stop_text`/`stop_capture` works for OpenRouter regex stop path.
- Streamed output and final capture values match deterministic rules.

## Cross-Cutting Implementation Steps
1. Add internal utilities for:
   - chunk logprobs normalization.
   - streaming regex stop matcher with deterministic emit boundaries.
2. Refactor OpenRouter rule path to use matcher and computed capture log probs.
3. Add tests in `tests/unit/` for utilities and rule behavior.
4. Add OpenRouter credentialed tests in `tests/need_credentials/`.
5. Document behavior in `README.md`/docs for OpenRouter caveats and support matrix.

## Rollout Strategy
- Phase 1:
  - Land unit-tested internal utilities.
  - Land logprobs request/parse/capture improvements.
- Phase 2:
  - Land client-side `stop_regex` + `stop_capture`.
  - Add credentialed smoke tests.
- Phase 3:
  - Update docs and release notes with compatibility table and examples.

## Risks and Mitigations
- Risk: Provider chunk schema drift for logprobs.
  - Mitigation: defensive parser + fallback to text-only path.
- Risk: Regex streaming matcher emits too early/late on boundary conditions.
  - Mitigation: exhaustive boundary-focused tests and deterministic match policy.
- Risk: Performance overhead from regex matching each chunk.
  - Mitigation: rolling-window strategy and optional micro-optimization after correctness.

## Definition of Done
- All new unit tests pass.
- Existing OpenRouter tests and unrelated model tests remain green.
- `guidance` can:
  - exploit logprobs/top-logprobs when truly supported,
  - expose accurate capture log probs where available,
  - support `stop_regex` + `stop_capture` in OpenRouter streaming mode.
