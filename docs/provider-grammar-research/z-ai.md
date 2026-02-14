## Provider
Z.AI (GLM models) via `POST /api/paas/v4/chat/completions`.

## Grammar capability
Official docs show **JSON mode only**, not grammar-constrained decoding.
- Supported response formats are `text` and `json_object`.
- I found **no documented support** for CFG/BNF/EBNF grammars, regex-constrained decoding, or a `json_schema` response format.

## Request shape
For structured output, documented request shape is:
- `response_format: { "type": "json_object" }`
- plus normal chat fields (`model`, `messages`, optional `stream`).

Example (documented pattern):
```json
{
  "model": "glm-5",
  "messages": [{"role":"user","content":"..."}],
  "response_format": { "type": "json_object" },
  "stream": true
}
```

## Grammar dialect and caveats
- **Dialect:** None documented (no grammar/regex/CFG dialect specified).
- **Caveat:** “Structured output” is described as JSON mode, and docs recommend describing expected JSON structure in prompts/system message; schema validation is shown as **client-side validation** in examples, not server-enforced decoding constraints.

## Streaming fields
Relevant documented SSE fields:
- `choices[0].delta.content` (incremental content)
- `choices[0].delta.reasoning_content` (incremental reasoning)
- `choices[0].finish_reason` (final chunk)
- `usage` (final chunk)
- stream ends with `data: [DONE]`

For constrained output use, JSON content arrives incrementally in `delta.content`; no extra grammar-state fields are documented.

## Sources (URLs)
- https://docs.z.ai/guides/capabilities/struct-output
- https://docs.z.ai/api-reference/llm/chat-completion
- https://docs.z.ai/guides/capabilities/streaming

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
session id: 019c5b0f-8fe5-74c1-a855-e39bb6a6c526
--------
user
Research official documentation for provider "Z.AI" focused on grammar-constrained generation.
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
2026-02-14T07:31:12.512806Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5531-6c60-7612-b81c-b02333263b22
2026-02-14T07:31:12.533569Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5080-050b-7c53-92a8-9c52ce325359
2026-02-14T07:31:12.554290Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c58f2-9999-7e13-8897-cb3cb6765c62
2026-02-14T07:31:12.575217Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5ae2-4d18-7921-a6f9-9ca09a337133
2026-02-14T07:31:12.595818Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-1e63-7422-8df1-29cc3cd854ed
2026-02-14T07:31:12.616482Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-2af1-7321-8d40-367f5a3ba03a
2026-02-14T07:31:12.637074Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-8eca-7cf3-8c60-d66e26ea0144
2026-02-14T07:31:12.657731Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-1935-7772-bf75-7eb9d084599e
2026-02-14T07:31:12.678853Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-45eb-7810-9be4-e9c813827907
2026-02-14T07:31:12.699967Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-5630-7b30-8723-45187528edea
2026-02-14T07:31:12.720570Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0a-f457-71d1-902a-d41b0df6fafa
2026-02-14T07:31:12.741469Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0a-f500-7013-80bc-cc4e70470657
2026-02-14T07:31:12.761982Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-1200-74e2-b68a-b5695adf8ddc
2026-02-14T07:31:12.782694Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-4f6c-79a1-ad3e-23dd8a997ea2
2026-02-14T07:31:12.803349Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e2-75e1-99f8-269a75536055
2026-02-14T07:31:12.823963Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e0-7850-aab6-44bd39f1876c
2026-02-14T07:31:12.844670Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e3-7490-b15b-7731fbbd70ff
2026-02-14T07:31:12.865238Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0e-b4b5-7fe2-a3e5-58d9a3aefdc9
2026-02-14T07:31:12.885866Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0e-ef2a-7fe1-acb9-0efdd7098be1
2026-02-14T07:31:12.906541Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0f-1210-7683-86d6-0b2317ac7328
2026-02-14T07:31:12.927184Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0f-1b55-7231-b650-1e96b003c19f
2026-02-14T07:31:12.947878Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0f-32f7-7891-bca9-59d526279265
mcp: surrealdb ready
mcp: playwright ready
mcp: exa ready
mcp startup: ready: surrealdb, playwright, exa

thinking
**Planning official docs search**
🌐 Searching the web...
🌐 Searched: Z.AI official API documentation grammar constrained decoding CFG regex

thinking
**Planning doc retrieval**
🌐 Searching the web...
🌐 Searched: https://docs.z.ai/guides/capabilities/struct-output

thinking
**Locating streaming fields info**
🌐 Searching the web...
🌐 Searched: https://docs.z.ai/guides/capabilities/streaming

thinking
**Inspecting API reference for request fields**
🌐 Searching the web...
🌐 Searched: https://docs.z.ai/api-reference/introduction

thinking
**Clarifying POST chat completion requirements**
🌐 Searching the web...
🌐 Searched: https://docs.z.ai/api-reference/llm/chat-completion

thinking
**Planning response_format search**
🌐 Searching the web...
🌐 Searched: 'response_format' in https://docs.z.ai/api-reference/llm/chat-completion

thinking
**Checking grammar support in docs**
🌐 Searching the web...
🌐 Searched: site:docs.z.ai "response_format" "json_object" "json_schema"

thinking
**Confirming no grammar support**
codex
## Provider
Z.AI (GLM models) via `POST /api/paas/v4/chat/completions`.

## Grammar capability
Official docs show **JSON mode only**, not grammar-constrained decoding.
- Supported response formats are `text` and `json_object`.
- I found **no documented support** for CFG/BNF/EBNF grammars, regex-constrained decoding, or a `json_schema` response format.

## Request shape
For structured output, documented request shape is:
- `response_format: { "type": "json_object" }`
- plus normal chat fields (`model`, `messages`, optional `stream`).

Example (documented pattern):
```json
{
  "model": "glm-5",
  "messages": [{"role":"user","content":"..."}],
  "response_format": { "type": "json_object" },
  "stream": true
}
```

## Grammar dialect and caveats
- **Dialect:** None documented (no grammar/regex/CFG dialect specified).
- **Caveat:** “Structured output” is described as JSON mode, and docs recommend describing expected JSON structure in prompts/system message; schema validation is shown as **client-side validation** in examples, not server-enforced decoding constraints.

## Streaming fields
Relevant documented SSE fields:
- `choices[0].delta.content` (incremental content)
- `choices[0].delta.reasoning_content` (incremental reasoning)
- `choices[0].finish_reason` (final chunk)
- `usage` (final chunk)
- stream ends with `data: [DONE]`

For constrained output use, JSON content arrives incrementally in `delta.content`; no extra grammar-state fields are documented.

## Sources (URLs)
- https://docs.z.ai/guides/capabilities/struct-output
- https://docs.z.ai/api-reference/llm/chat-completion
- https://docs.z.ai/guides/capabilities/streaming
tokens used
27,403
```

