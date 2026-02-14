# Grammar Integration Docs Index

This index organizes the current Markdown documentation for grammar/constrained-generation integration work.

## Metadata

- Status: current
- Last updated: 2026-02-13
- Maintainer scope: OpenAI/Fireworks/OpenRouter grammar integration docs

## Current Canonical Docs

1. `docs/openai-fireworks-openrouter-grammar-worklog.md`
   - End-to-end implementation + research log.
   - Includes links consulted, design decisions, live test outcomes, and follow-up actions.

2. `docs/openrouter-capabilities.md`
   - OpenRouter capability resolution behavior, runtime gates, and request-shaping policy.

3. `docs/openrouter-grammar-findings.md`
   - OpenRouter grammar-specific findings, probe summaries, and known variability.

4. `docs/openrouter-provider-grammar-capabilities.md`
   - Latest provider capability discovery summary generated from low-cost model probes.

## Supporting Artifacts

1. `docs/openrouter-grammar-probe-matrix.md`
   - Human-readable provider/format probe results.

2. `docs/openrouter-grammar-probe-matrix.json`
   - Machine-readable probe results.

3. `docs/fireworks-sdk-grammar-investigation.md`
   - Fireworks SDK + live stream behavior findings for grammar mode.
   - Documents `reasoning_content` nuance and OpenRouter applicability.

4. `guidance/resources/openrouter_provider_grammar_capabilities.json`
   - Shipped machine-readable provider grammar capability cache used at runtime.

5. `docs/openrouter-provider-grammar-raw-outputs.json`
   - Raw non-stream and stream payload captures used to validate provider classification.

6. `docs/provider-grammar-research-matrix.md`
   - Consolidated provider-docs compatibility matrix (support level, dialect, request shape, streaming fields).

7. `docs/provider-grammar-research-matrix.json`
   - Machine-readable version of the provider-docs matrix.

## Plan / Historical Docs

1. `docs/openai-fireworks-native-grammar-implementation-plan.md`
   - Original implementation plan plus implementation-status notes.
   - Kept for planning traceability.

2. `docs/openrouter-logprobs-stop-regex-implementation-plan.md`
   - Earlier OpenRouter-focused implementation plan (historical reference).

## Recommended Reading Order

1. `docs/openai-fireworks-openrouter-grammar-worklog.md`
2. `docs/openrouter-capabilities.md`
3. `docs/openrouter-grammar-findings.md`
4. `docs/openrouter-grammar-probe-matrix.md` (and `.json` if needed)
