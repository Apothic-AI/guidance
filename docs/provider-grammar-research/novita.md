## Provider
**Novita AI** (`https://api.novita.ai/openai/v1/chat/completions` OpenAI-compatible Chat Completions).

## Grammar capability
- **Documented support:** `response_format: { "type": "json_schema", ... }` (Structured Outputs).
- **Also available:** `response_format: { "type": "json_object" }` (older JSON mode).
- **Not explicitly documented:** CFG/BNF grammar constraints or regex-constrained decoding fields.
- **Inference from docs/search:** Novita documents JSON Schema-based constraints, not generic grammar/regex decoders.

## Request shape
Use Chat Completions with `response_format`:
```json
{
  "model": "…",
  "messages": [ ... ],
  "stream": true,
  "stream_options": { "include_usage": true },
  "response_format": {
    "type": "json_schema",
    "json_schema": {
      "name": "your_schema_name",
      "description": "optional",
      "schema": { "...": "JSON Schema object" },
      "strict": true
    }
  }
}
```
Notes:
- `response_format.type` enum: `text | json_object | json_schema`.
- `json_schema` object is required when `type = "json_schema"`.

## Grammar dialect and caveats
- Dialect is **JSON Schema-style structured output** (not CFG/regex grammar).
- Documented schema-supported types include: `string`, `number`, `integer`, `boolean`, `array`, `object`, `enum`, `anyOf`.
- With `strict: true`: Novita says **only a subset of JSON Schema is supported**; unsupported schema returns an error.

## Streaming fields
Relevant streaming behavior/fields:
- `stream: true` enables SSE token streaming, terminated by `data: [DONE]`.
- `stream_options.include_usage: true` adds an extra chunk before `[DONE]`:
  - this chunk has full `usage`,
  - `choices` is an empty array.
- Other streamed chunks include `usage: null`.
- Docs also state for streaming responses, `usage` appears in the last response chunk.

## Sources (URLs)
- https://novita.ai/docs/api-reference/model-apis-llm-create-chat-completion
- https://novita.ai/docs/guides/llm-structured-outputs
- https://novita.ai/docs/guides/llm-playgrounds

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
session id: 019c5b0e-7fe1-7683-ad3b-c244133d6497
--------
user
Research official documentation for provider "Novita" focused on grammar-constrained generation.
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
2026-02-14T07:30:02.874035Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5531-6c60-7612-b81c-b02333263b22
2026-02-14T07:30:02.894848Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5080-050b-7c53-92a8-9c52ce325359
2026-02-14T07:30:02.915788Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c58f2-9999-7e13-8897-cb3cb6765c62
2026-02-14T07:30:02.936393Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5ae2-4d18-7921-a6f9-9ca09a337133
2026-02-14T07:30:02.957151Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-1e63-7422-8df1-29cc3cd854ed
2026-02-14T07:30:02.978015Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-2af1-7321-8d40-367f5a3ba03a
2026-02-14T07:30:02.998917Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-8eca-7cf3-8c60-d66e26ea0144
2026-02-14T07:30:03.019687Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-1935-7772-bf75-7eb9d084599e
2026-02-14T07:30:03.040308Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-45eb-7810-9be4-e9c813827907
2026-02-14T07:30:03.061368Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-5630-7b30-8723-45187528edea
2026-02-14T07:30:03.082062Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0a-f457-71d1-902a-d41b0df6fafa
2026-02-14T07:30:03.102751Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0a-f500-7013-80bc-cc4e70470657
2026-02-14T07:30:03.123533Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-1200-74e2-b68a-b5695adf8ddc
2026-02-14T07:30:03.144513Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-4f6c-79a1-ad3e-23dd8a997ea2
2026-02-14T07:30:03.165214Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e2-75e1-99f8-269a75536055
2026-02-14T07:30:03.185824Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e0-7850-aab6-44bd39f1876c
2026-02-14T07:30:03.206448Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e3-7490-b15b-7731fbbd70ff
2026-02-14T07:30:03.227230Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0d-db4c-7cc2-99b4-a433007462d2
2026-02-14T07:30:03.247882Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0d-f508-7283-bcc5-b2effda3a024
2026-02-14T07:30:03.268498Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0e-2f50-7813-ba50-182d396da368
2026-02-14T07:30:03.289137Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0e-4762-75c1-b6a7-713ce89707a2
2026-02-14T07:30:03.310080Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0e-4ff4-7c11-809c-677b76971da0
mcp: surrealdb ready
mcp: playwright ready
mcp: exa ready
mcp startup: ready: surrealdb, playwright, exa
🌐 Searching the web...
🌐 Searched: Novita AI documentation grammar constrained decoding CFG regex structured outputs

thinking
**Checking streaming and output schema details**
codex
I’m checking Novita’s official API docs directly now to confirm exactly what constrained-decoding modes they expose and what streaming fields are documented.
🌐 Searching the web...
🌐 Searched: https://novita.ai/docs/api-reference/model-apis-llm-create-chat-completion

thinking
**Seeking schema pattern**
🌐 Searching the web...
🌐 Searched: 'Supported models' in https://novita.ai/docs/guides/llm-structured-outputs

thinking
**Assessing streaming response schema**
codex
I confirmed the main chat-completions schema and structured-output guide. Next I’m extracting the exact streaming chunk fields and any explicit limits/caveats on strict schema mode.
🌐 Searching the web...
🌐 Searched: 'include_usage' in https://novita.ai/docs/api-reference/model-apis-llm-create-chat-completion

thinking
**Searching for regex support**
🌐 Searching the web...
🌐 Searched: site:novita.ai/docs Novita regex constrained decoding

thinking
**Summarizing doc search and output constraints**
codex
## Provider
**Novita AI** (`https://api.novita.ai/openai/v1/chat/completions` OpenAI-compatible Chat Completions).

## Grammar capability
- **Documented support:** `response_format: { "type": "json_schema", ... }` (Structured Outputs).
- **Also available:** `response_format: { "type": "json_object" }` (older JSON mode).
- **Not explicitly documented:** CFG/BNF grammar constraints or regex-constrained decoding fields.
- **Inference from docs/search:** Novita documents JSON Schema-based constraints, not generic grammar/regex decoders.

## Request shape
Use Chat Completions with `response_format`:
```json
{
  "model": "…",
  "messages": [ ... ],
  "stream": true,
  "stream_options": { "include_usage": true },
  "response_format": {
    "type": "json_schema",
    "json_schema": {
      "name": "your_schema_name",
      "description": "optional",
      "schema": { "...": "JSON Schema object" },
      "strict": true
    }
  }
}
```
Notes:
- `response_format.type` enum: `text | json_object | json_schema`.
- `json_schema` object is required when `type = "json_schema"`.

## Grammar dialect and caveats
- Dialect is **JSON Schema-style structured output** (not CFG/regex grammar).
- Documented schema-supported types include: `string`, `number`, `integer`, `boolean`, `array`, `object`, `enum`, `anyOf`.
- With `strict: true`: Novita says **only a subset of JSON Schema is supported**; unsupported schema returns an error.

## Streaming fields
Relevant streaming behavior/fields:
- `stream: true` enables SSE token streaming, terminated by `data: [DONE]`.
- `stream_options.include_usage: true` adds an extra chunk before `[DONE]`:
  - this chunk has full `usage`,
  - `choices` is an empty array.
- Other streamed chunks include `usage: null`.
- Docs also state for streaming responses, `usage` appears in the last response chunk.

## Sources (URLs)
- https://novita.ai/docs/api-reference/model-apis-llm-create-chat-completion
- https://novita.ai/docs/guides/llm-structured-outputs
- https://novita.ai/docs/guides/llm-playgrounds
tokens used
33,004
```

