## Provider
**FriendliAI** (Friendli Docs; OpenAI-compatible chat/completions APIs).

## Grammar capability
- **Supported constrained output modes:** `response_format.type` = `json_schema`, `json_object`, `regex` (and `text`).
- **Regex-constrained decoding:** documented via `type: "regex"` with a regex `schema`.
- **CFG/grammar (EBNF/GBNF) decoding:** **not documented** in official docs I found (no explicit CFG grammar interface; constraints are via JSON Schema or regex).

## Request shape
For chat completions (`/serverless/v1/chat/completions` and dedicated equivalent), constraints are passed in `response_format`:

- JSON Schema:
```json
{
  "response_format": {
    "type": "json_schema",
    "json_schema": { "schema": { "...": "..." } }
  }
}
```

- JSON mode:
```json
{ "response_format": { "type": "json_object" } }
```

- Regex mode:
```json
{
  "response_format": {
    "type": "regex",
    "schema": "YOUR_REGEX_PATTERN"
  }
}
```

Relevant documented interactions:
- `tools` + `response_format` are incompatible.
- `response_format` + `min_tokens` are incompatible.
- Must explicitly prompt model to output the target format (otherwise malformed/degenerate output risk).

## Grammar dialect and caveats
- **Regex dialect:** documented as “regex” but engine/dialect specifics are **not clearly specified**.
- **JSON Schema support is partial/subset**, including key caveats:
  - 7 base types supported.
  - `anyOf` supported; other composition forms not promised.
  - `$ref` only for internal subschemas in `$defs`.
  - `additionalProperties` is ignored and treated as false.
  - `minItems` only supports `0` or `1`.
  - annotations like `title`/`description` accepted but ignored.
- Output can still truncate at `max_tokens` (`finish_reason: "length"`).

## Streaming fields
With `stream: true`, response is SSE (`text/event-stream`), chunk object `chat.completion.chunk`:
- `choices[].delta.role`
- `choices[].delta.content`
- `choices[].delta.tool_calls` (if tool flow)
- `choices[].finish_reason` (`stop`, `length`, `tool_calls`, or `null` mid-stream)
- `usage` appears as `null` in token chunks and as usage object in a terminal chunk, followed by `data: [DONE]`.

## Sources (URLs)
- https://friendli.ai/docs/openapi/serverless/chat-completions
- https://friendli.ai/docs/openapi/dedicated/inference/chat-completions
- https://friendli.ai/docs/guides/structured-outputs
- https://friendli.ai/docs/openapi/dedicated/inference/chat-completions-chunk-object
- https://friendli.ai/docs/openapi/serverless/tool-assisted-chat-completions-chunk-object

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
session id: 019c5b0d-db4c-7cc2-99b4-a433007462d2
--------
user
Research official documentation for provider "Friendli" focused on grammar-constrained generation.
Find whether they support grammar/CFG/regex constrained decoding, exact request fields, grammar dialect,
and streaming response fields relevant to constrained output.

Return concise markdown with sections:
- Provider
- Grammar capability
- Request shape
- Grammar dialect and caveats
- Streaming fields
- Sources (URLs)
mcp: exa starting
mcp: surrealdb starting
mcp: playwright starting
2026-02-14T07:29:20.763345Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5531-6c60-7612-b81c-b02333263b22
2026-02-14T07:29:20.785749Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5080-050b-7c53-92a8-9c52ce325359
2026-02-14T07:29:20.806484Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c58f2-9999-7e13-8897-cb3cb6765c62
2026-02-14T07:29:20.827438Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5ae2-4d18-7921-a6f9-9ca09a337133
2026-02-14T07:29:20.848152Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-1e63-7422-8df1-29cc3cd854ed
2026-02-14T07:29:20.868855Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-2af1-7321-8d40-367f5a3ba03a
2026-02-14T07:29:20.889689Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-8eca-7cf3-8c60-d66e26ea0144
2026-02-14T07:29:20.910485Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-1935-7772-bf75-7eb9d084599e
2026-02-14T07:29:20.931070Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-45eb-7810-9be4-e9c813827907
2026-02-14T07:29:20.951691Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-5630-7b30-8723-45187528edea
2026-02-14T07:29:20.972586Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0a-f457-71d1-902a-d41b0df6fafa
2026-02-14T07:29:20.993524Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0a-f500-7013-80bc-cc4e70470657
2026-02-14T07:29:21.014317Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-1200-74e2-b68a-b5695adf8ddc
2026-02-14T07:29:21.034969Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-4f6c-79a1-ad3e-23dd8a997ea2
2026-02-14T07:29:21.055514Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e2-75e1-99f8-269a75536055
2026-02-14T07:29:21.076129Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e0-7850-aab6-44bd39f1876c
2026-02-14T07:29:21.096797Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e3-7490-b15b-7731fbbd70ff
2026-02-14T07:29:21.117327Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-fd96-7c40-9fb5-4533f503a218
2026-02-14T07:29:21.137950Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-fd89-7162-9102-1207ec15728d
2026-02-14T07:29:21.158869Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-fd87-77a2-b52d-3b01e53fde37
2026-02-14T07:29:21.179628Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-fd87-7a13-a28a-bd0bb5eb39b5
2026-02-14T07:29:21.200530Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-fd86-7282-9d41-25a8785365db
mcp: surrealdb ready
mcp: playwright ready
mcp: exa ready
mcp startup: ready: surrealdb, playwright, exa
🌐 Searching the web...
🌐 Searched: Friendli official documentation grammar constrained generation regex CFG constrained decoding

thinking
**Expanding search beyond docs**
🌐 Searching the web...
🌐 Searched: Friendli API documentation constrained decoding grammar regex CFG

thinking
**Reviewing OpenAPI response_format details**
🌐 Searching the web...
🌐 Searched: https://friendli.ai/docs/openapi/dedicated/inference/chat-completions

thinking
**Checking full response format**
🌐 Searching the web...
🌐 Searched: 'response_format' in https://friendli.ai/docs/openapi/dedicated/inference/chat-completions

thinking
**Accessing link details**
🌐 Searching the web...
🌐 Searched: https://friendli.ai/docs/guides/serverless_endpoints/structured-outputs

thinking
**Searching for response field patterns**
🌐 Searching the web...
🌐 Searched: 'delta' in https://friendli.ai/docs/openapi/dedicated/inference/chat-completions-chunk-object

thinking
**Checking grammar constraint support**
🌐 Searching the web...
🌐 Searched: site:friendli.ai/docs CFG constrained decoding Friendli

thinking
**Exploring streaming field handling**
🌐 Searching the web...
🌐 Searched: site:friendli.ai/docs chat completions chunk object serverless

thinking
**Investigating request fields and dialect**
🌐 Searching the web...
🌐 Searched: https://friendli.ai/docs/openapi/serverless/chat-completions

thinking
**Separating reference ID lookup calls**
🌐 Searching the web...
🌐 Searched: 'response_format' in https://friendli.ai/docs/openapi/serverless/chat-completions

thinking
**Investigating response format details**
🌐 Searching the web...
🌐 Searched: friendli openapi json serverless v1 chat completions response_format regex schema field

thinking
**Summarizing request schema and streaming details**
codex
## Provider
**FriendliAI** (Friendli Docs; OpenAI-compatible chat/completions APIs).

## Grammar capability
- **Supported constrained output modes:** `response_format.type` = `json_schema`, `json_object`, `regex` (and `text`).
- **Regex-constrained decoding:** documented via `type: "regex"` with a regex `schema`.
- **CFG/grammar (EBNF/GBNF) decoding:** **not documented** in official docs I found (no explicit CFG grammar interface; constraints are via JSON Schema or regex).

## Request shape
For chat completions (`/serverless/v1/chat/completions` and dedicated equivalent), constraints are passed in `response_format`:

- JSON Schema:
```json
{
  "response_format": {
    "type": "json_schema",
    "json_schema": { "schema": { "...": "..." } }
  }
}
```

- JSON mode:
```json
{ "response_format": { "type": "json_object" } }
```

- Regex mode:
```json
{
  "response_format": {
    "type": "regex",
    "schema": "YOUR_REGEX_PATTERN"
  }
}
```

Relevant documented interactions:
- `tools` + `response_format` are incompatible.
- `response_format` + `min_tokens` are incompatible.
- Must explicitly prompt model to output the target format (otherwise malformed/degenerate output risk).

## Grammar dialect and caveats
- **Regex dialect:** documented as “regex” but engine/dialect specifics are **not clearly specified**.
- **JSON Schema support is partial/subset**, including key caveats:
  - 7 base types supported.
  - `anyOf` supported; other composition forms not promised.
  - `$ref` only for internal subschemas in `$defs`.
  - `additionalProperties` is ignored and treated as false.
  - `minItems` only supports `0` or `1`.
  - annotations like `title`/`description` accepted but ignored.
- Output can still truncate at `max_tokens` (`finish_reason: "length"`).

## Streaming fields
With `stream: true`, response is SSE (`text/event-stream`), chunk object `chat.completion.chunk`:
- `choices[].delta.role`
- `choices[].delta.content`
- `choices[].delta.tool_calls` (if tool flow)
- `choices[].finish_reason` (`stop`, `length`, `tool_calls`, or `null` mid-stream)
- `usage` appears as `null` in token chunks and as usage object in a terminal chunk, followed by `data: [DONE]`.

## Sources (URLs)
- https://friendli.ai/docs/openapi/serverless/chat-completions
- https://friendli.ai/docs/openapi/dedicated/inference/chat-completions
- https://friendli.ai/docs/guides/structured-outputs
- https://friendli.ai/docs/openapi/dedicated/inference/chat-completions-chunk-object
- https://friendli.ai/docs/openapi/serverless/tool-assisted-chat-completions-chunk-object
tokens used
53,752
```

