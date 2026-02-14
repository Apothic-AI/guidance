## Provider
**Together AI** (`https://api.together.xyz/v1`, OpenAI-compatible Chat Completions API).

## Grammar capability
- **Supported (officially documented):**
  - JSON Schema-constrained output
  - Regex-constrained output
- **Not clearly documented as supported:** explicit **CFG/BNF grammar decoding** (no dedicated CFG field in Together docs I found).

## Request shape
- JSON Schema mode:
```json
"response_format": {
  "type": "json_schema",
  "schema": { "...": "JSON Schema object" }
}
```
- Regex mode:
```json
"response_format": {
  "type": "regex",
  "pattern": "(positive|neutral|negative)"
}
```
- Also documented in API reference/OpenAI-compat context: `response_format.type` variants include text/json-object/json-schema styles.

## Grammar dialect and caveats
- **JSON mode dialect:** standard **JSON Schema object** passed in `response_format`.
- **Regex dialect:** standard regex string in `pattern` (docs show examples only; no formal regex-engine spec on that page).
- **Caveat:** Together docs show both OpenAI-compatible language and Together-native examples; field naming around schema may appear in different forms across pages (`schema` in structured-output examples vs OpenAI-style docs elsewhere). Validate against your target SDK version.
- **Prompting caveat (explicitly documented):** they recommend also instructing the model in prompt text to answer in JSON and include schema text, in addition to `response_format`.

## Streaming fields
Relevant streamed fields for constrained output assembly:
- `chunk.choices[0].delta.content` (token chunks of final output)
- For thinking models (e.g., Kimi K2 Thinking), also `chunk.choices[0].delta.reasoning`
- Streaming enabled with `stream=true`; together examples iterate over `chunk.choices[0].delta...`

## Sources (URLs)
- https://docs.together.ai/docs/json-mode
- https://docs.together.ai/docs/openai-api-compatibility
- https://docs.together.ai/docs/chat-overview
- https://docs.together.ai/docs/kimi-k2-thinking-quickstart
- https://docs.together.ai/reference/

## stderr
```
OpenAI Codex v0.101.0 (research preview)
--------
workdir: /home/bitnom/Code/apothic-monorepo/libs/python/guidance
model: gpt-5.3-codex
provider: openai
approval: never
sandbox: danger-full-access
reasoning effort: low
reasoning summaries: auto
session id: 019c5b0f-1210-7683-86d6-0b2317ac7328
--------
user
Research official documentation for provider "Together" focused on grammar-constrained generation.
Find whether they support grammar/CFG/regex constrained decoding, exact request fields, grammar dialect,
and streaming response fields relevant to constrained output.

Return concise markdown with sections:
- Provider
- Grammar capability
- Request shape
- Grammar dialect and caveats
- Streaming fields
- Sources (URLs)
mcp: playwright starting
mcp: surrealdb starting
mcp: exa starting
2026-02-14T07:30:40.298820Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5531-6c60-7612-b81c-b02333263b22
2026-02-14T07:30:40.321552Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5080-050b-7c53-92a8-9c52ce325359
2026-02-14T07:30:40.342155Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c58f2-9999-7e13-8897-cb3cb6765c62
2026-02-14T07:30:40.362967Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5ae2-4d18-7921-a6f9-9ca09a337133
2026-02-14T07:30:40.383567Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-1e63-7422-8df1-29cc3cd854ed
2026-02-14T07:30:40.404122Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-2af1-7321-8d40-367f5a3ba03a
2026-02-14T07:30:40.424794Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-8eca-7cf3-8c60-d66e26ea0144
2026-02-14T07:30:40.445348Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-1935-7772-bf75-7eb9d084599e
2026-02-14T07:30:40.465960Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-45eb-7810-9be4-e9c813827907
2026-02-14T07:30:40.486708Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-5630-7b30-8723-45187528edea
2026-02-14T07:30:40.507437Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0a-f457-71d1-902a-d41b0df6fafa
2026-02-14T07:30:40.528103Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0a-f500-7013-80bc-cc4e70470657
2026-02-14T07:30:40.548843Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-1200-74e2-b68a-b5695adf8ddc
2026-02-14T07:30:40.569476Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-4f6c-79a1-ad3e-23dd8a997ea2
2026-02-14T07:30:40.590213Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e2-75e1-99f8-269a75536055
2026-02-14T07:30:40.610921Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e0-7850-aab6-44bd39f1876c
2026-02-14T07:30:40.631704Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e3-7490-b15b-7731fbbd70ff
2026-02-14T07:30:40.652409Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0e-4762-75c1-b6a7-713ce89707a2
2026-02-14T07:30:40.672985Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0e-4ff4-7c11-809c-677b76971da0
2026-02-14T07:30:40.693758Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0e-b4b5-7fe2-a3e5-58d9a3aefdc9
2026-02-14T07:30:40.714538Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0e-b66a-79c1-a388-4af5a76df995
2026-02-14T07:30:40.735343Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0e-ef2a-7fe1-acb9-0efdd7098be1
mcp: surrealdb ready
mcp: playwright ready
mcp: exa ready
mcp startup: ready: surrealdb, playwright, exa
codex
I’ll verify this directly from Together’s official docs and extract the exact constrained-decoding fields, grammar format, and streaming payload details. I’m starting with targeted doc searches, then I’ll open the relevant API reference pages.
🌐 Searching the web...
🌐 Searched: Together AI official documentation grammar constrained decoding JSON schema regex CFG

thinking
**Searching Together docs for streaming**
codex
I found Together’s official Structured Outputs page with concrete `response_format` fields. Next I’m pulling Together’s own streaming reference to confirm chunk/`delta` fields for constrained output.
🌐 Searching the web...
🌐 Searched: site:docs.together.ai Together streaming chat completions chunk delta usage include_usage

thinking
**Exploring response format details**
🌐 Searching the web...
🌐 Searched: https://docs.together.ai/reference/

thinking
**Identifying correct API docs endpoint**
🌐 Searching the web...
🌐 Searched: site:docs.together.ai/reference chat completions response_format type regex json_schema

thinking
**Reviewing streaming response schema**
codex
I now have the main constrained-output page and will extract exact `response_format` variants from it. I’ll also verify if Together documents CFG specifically or only regex/JSON-schema modes.
🌐 Searching the web...
🌐 Searched: https://docs.together.ai/docs/json-mode

thinking
**Reviewing streaming fields**
codex
I confirmed Together documents `json_schema` and `regex` directly; I haven’t found any official CFG/BNF grammar endpoint yet. I’m now extracting the streaming chunk fields from Together’s Chat/OpenAI-compatibility pages and model quickstarts.
🌐 Searching the web...
🌐 Searched: https://docs.together.ai/docs/openai-api-compatibility

thinking
**Planning targeted line extraction**
🌐 Searching the web...
🌐 Searched: https://docs.together.ai/docs/chat-overview

thinking
**Clarifying response format inconsistencies**
codex
## Provider
**Together AI** (`https://api.together.xyz/v1`, OpenAI-compatible Chat Completions API).

## Grammar capability
- **Supported (officially documented):**
  - JSON Schema-constrained output
  - Regex-constrained output
- **Not clearly documented as supported:** explicit **CFG/BNF grammar decoding** (no dedicated CFG field in Together docs I found).

## Request shape
- JSON Schema mode:
```json
"response_format": {
  "type": "json_schema",
  "schema": { "...": "JSON Schema object" }
}
```
- Regex mode:
```json
"response_format": {
  "type": "regex",
  "pattern": "(positive|neutral|negative)"
}
```
- Also documented in API reference/OpenAI-compat context: `response_format.type` variants include text/json-object/json-schema styles.

## Grammar dialect and caveats
- **JSON mode dialect:** standard **JSON Schema object** passed in `response_format`.
- **Regex dialect:** standard regex string in `pattern` (docs show examples only; no formal regex-engine spec on that page).
- **Caveat:** Together docs show both OpenAI-compatible language and Together-native examples; field naming around schema may appear in different forms across pages (`schema` in structured-output examples vs OpenAI-style docs elsewhere). Validate against your target SDK version.
- **Prompting caveat (explicitly documented):** they recommend also instructing the model in prompt text to answer in JSON and include schema text, in addition to `response_format`.

## Streaming fields
Relevant streamed fields for constrained output assembly:
- `chunk.choices[0].delta.content` (token chunks of final output)
- For thinking models (e.g., Kimi K2 Thinking), also `chunk.choices[0].delta.reasoning`
- Streaming enabled with `stream=true`; together examples iterate over `chunk.choices[0].delta...`

## Sources (URLs)
- https://docs.together.ai/docs/json-mode
- https://docs.together.ai/docs/openai-api-compatibility
- https://docs.together.ai/docs/chat-overview
- https://docs.together.ai/docs/kimi-k2-thinking-quickstart
- https://docs.together.ai/reference/
tokens used
30,810
```

