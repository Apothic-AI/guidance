## Provider
Alibaba Cloud Model Studio (Qwen APIs), via:
- OpenAI-compatible Chat Completions endpoint
- DashScope native endpoint

## Grammar capability
- **Documented constrained output is JSON-focused only**:
  - `json_object` mode (valid JSON string, schema not guaranteed)
  - `json_schema` mode (schema-conformant JSON)
- I found **no official Alibaba fields for CFG/EBNF/regex-constrained decoding** in these API docs.
- Structured output is documented as **not supported in thinking mode**.

## Request shape
- Main field: `response_format`  
- Values:
  - `{"type":"json_object"}`
  - `{"type":"json_schema","json_schema":{...}}`
- `json_schema` object fields (documented):
  - `name` (required)
  - `description` (optional)
  - `schema` (JSON Schema object)
  - `strict` (optional, default `false`, `true` recommended)
- Streaming controls:
  - `stream: true`
  - `stream_options: {"include_usage": true|false}`

## Grammar dialect and caveats
- Dialect is **JSON Schema** (not CFG/regex grammar syntax).
- Structured output docs explicitly describe only JSON Object / JSON Schema.
- Caveats:
  - For `json_object`, prompt must include “JSON” keyword or request errors.
  - `strict: true` is recommended for strict compliance.
  - Supported types called out: `string`, `number`, `integer`, `boolean`, `object`, `array`, `enum`.
  - Thinking mode: structured output unsupported; docs warn not to set `response_format={"type":"json_object"}` in thinking mode.
  - Docs advise avoiding `max_tokens` with structured output to reduce incomplete JSON risk.

## Streaming fields
Relevant chunk fields when consuming constrained output via streaming:
- `choices[].delta.content` (append across chunks to reconstruct output text/JSON)
- `choices[].finish_reason` (`stop`, `null`, `length`, `tool_calls`)
- `choices[].delta.role` (typically present in first chunk)
- `usage` appears in final chunk if `stream_options.include_usage=true`; in that last usage chunk, `choices` can be empty.

## Sources (URLs)
- https://www.alibabacloud.com/help/en/model-studio/qwen-structured-output
- https://www.alibabacloud.com/help/en/model-studio/qwen-api-via-openai-chat-completions
- https://www.alibabacloud.com/help/en/model-studio/qwen-api-reference/

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
session id: 019c5b0c-fd86-7282-9d41-25a8785365db
--------
user
Research official documentation for provider "Alibaba" focused on grammar-constrained generation.
Find whether they support grammar/CFG/regex constrained decoding, exact request fields, grammar dialect,
and streaming response fields relevant to constrained output.

Return concise markdown with sections:
- Provider
- Grammar capability
- Request shape
- Grammar dialect and caveats
- Streaming fields
- Sources (URLs)
mcp: surrealdb starting
mcp: exa starting
mcp: playwright starting
2026-02-14T07:28:23.978934Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5531-6c60-7612-b81c-b02333263b22
2026-02-14T07:28:24.028100Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5080-050b-7c53-92a8-9c52ce325359
2026-02-14T07:28:24.065117Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c58f2-9999-7e13-8897-cb3cb6765c62
2026-02-14T07:28:24.083934Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5ae2-4d18-7921-a6f9-9ca09a337133
2026-02-14T07:28:24.112841Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-1e63-7422-8df1-29cc3cd854ed
2026-02-14T07:28:24.143021Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-2af1-7321-8d40-367f5a3ba03a
2026-02-14T07:28:24.180210Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-8eca-7cf3-8c60-d66e26ea0144
2026-02-14T07:28:24.198682Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-1935-7772-bf75-7eb9d084599e
2026-02-14T07:28:24.221244Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-45eb-7810-9be4-e9c813827907
2026-02-14T07:28:24.259441Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-5630-7b30-8723-45187528edea
2026-02-14T07:28:24.301434Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0a-f457-71d1-902a-d41b0df6fafa
2026-02-14T07:28:24.341551Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0a-f500-7013-80bc-cc4e70470657
2026-02-14T07:28:24.365183Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-1200-74e2-b68a-b5695adf8ddc
2026-02-14T07:28:24.405154Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-4f6c-79a1-ad3e-23dd8a997ea2
2026-02-14T07:28:24.433890Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e2-75e1-99f8-269a75536055
2026-02-14T07:28:24.464882Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e0-7850-aab6-44bd39f1876c
2026-02-14T07:28:24.485862Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e3-7490-b15b-7731fbbd70ff
mcp: surrealdb ready
mcp: playwright ready
mcp: exa ready
mcp startup: ready: surrealdb, playwright, exa
🌐 Searching the web...
🌐 Searched: Alibaba Cloud DashScope grammar constrained decoding CFG regex request fields official documentation

thinking
**Checking official documentation**
🌐 Searching the web...
🌐 Searched: https://www.alibabacloud.com/help/en/model-studio/developer-reference/qwen-model-api-details

thinking
**Planning targeted search strategy**
🌐 Searching the web...
🌐 Searched: site:alibabacloud.com/help model studio response_format json_schema qwen

thinking
**Identifying streaming fields in API docs**
🌐 Searching the web...
🌐 Searched: https://www.alibabacloud.com/help/en/model-studio/qwen-api-via-openai-chat-completions

thinking
**Searching config for grammar patterns**
🌐 Searching the web...
🌐 Searched: 'regex' in https://www.alibabacloud.com/help/en/model-studio/qwen-structured-output

thinking
**Exploring JSON schema properties**
🌐 Searching the web...
🌐 Searched: https://www.alibabacloud.com/help/en/model-studio/qwen-api-via-openai-chat-completions

thinking
**Assessing streaming field requirements**
🌐 Searching the web...
🌐 Searched: 'stream' in https://www.alibabacloud.com/help/en/model-studio/qwen-structured-output

thinking
**Verifying API response format support**
🌐 Searching the web...
🌐 Searched: https://www.alibabacloud.com/help/en/model-studio/qwen-api-via-openai-chat-completions

thinking
**Searching region support messages**
🌐 Searching the web...
🌐 Searched: 'Models in the Singapore region are not supported' in https://www.alibabacloud.com/help/en/model-studio/qwen-structured-output

thinking
**Identifying JSON Schema section**
🌐 Searching the web...
🌐 Searched: https://www.alibabacloud.com/help/en/model-studio/qwen-structured-output

thinking
**Confirming response_format constraints**
codex
## Provider
Alibaba Cloud Model Studio (Qwen APIs), via:
- OpenAI-compatible Chat Completions endpoint
- DashScope native endpoint

## Grammar capability
- **Documented constrained output is JSON-focused only**:
  - `json_object` mode (valid JSON string, schema not guaranteed)
  - `json_schema` mode (schema-conformant JSON)
- I found **no official Alibaba fields for CFG/EBNF/regex-constrained decoding** in these API docs.
- Structured output is documented as **not supported in thinking mode**.

## Request shape
- Main field: `response_format`  
- Values:
  - `{"type":"json_object"}`
  - `{"type":"json_schema","json_schema":{...}}`
- `json_schema` object fields (documented):
  - `name` (required)
  - `description` (optional)
  - `schema` (JSON Schema object)
  - `strict` (optional, default `false`, `true` recommended)
- Streaming controls:
  - `stream: true`
  - `stream_options: {"include_usage": true|false}`

## Grammar dialect and caveats
- Dialect is **JSON Schema** (not CFG/regex grammar syntax).
- Structured output docs explicitly describe only JSON Object / JSON Schema.
- Caveats:
  - For `json_object`, prompt must include “JSON” keyword or request errors.
  - `strict: true` is recommended for strict compliance.
  - Supported types called out: `string`, `number`, `integer`, `boolean`, `object`, `array`, `enum`.
  - Thinking mode: structured output unsupported; docs warn not to set `response_format={"type":"json_object"}` in thinking mode.
  - Docs advise avoiding `max_tokens` with structured output to reduce incomplete JSON risk.

## Streaming fields
Relevant chunk fields when consuming constrained output via streaming:
- `choices[].delta.content` (append across chunks to reconstruct output text/JSON)
- `choices[].finish_reason` (`stop`, `null`, `length`, `tool_calls`)
- `choices[].delta.role` (typically present in first chunk)
- `usage` appears in final chunk if `stream_options.include_usage=true`; in that last usage chunk, `choices` can be empty.

## Sources (URLs)
- https://www.alibabacloud.com/help/en/model-studio/qwen-structured-output
- https://www.alibabacloud.com/help/en/model-studio/qwen-api-via-openai-chat-completions
- https://www.alibabacloud.com/help/en/model-studio/qwen-api-reference/
tokens used
39,957
```

