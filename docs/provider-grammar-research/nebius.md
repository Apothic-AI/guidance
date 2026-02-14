## Provider
Nebius (currently branded in docs as **Nebius Token Factory**, OpenAI-compatible API at `https://api.tokenfactory.nebius.com/v1`).

## Grammar capability
- **Documented support:** structured JSON output via `response_format`.
- **Not explicitly documented:** CFG grammar constraints, regex-constrained decoding, or EBNF/GBNF-style grammar fields.
- I found no official Nebius doc fields named like `guided_regex`, `guided_grammar`, `grammar`, or `regex` in chat/completions docs.

## Request shape
- Main endpoint: `POST /v1/chat/completions`
- Relevant fields:
  - `response_format` (documented values vary by page):
    - Structured output page: `{"type":"json_schema","json_schema":...}` and `{"type":"json_object"}`
    - API reference page for chat completions: says only `{'type':'json_object'}` or `{'type':'text'}`
  - `extra_body`: generic object “to provide extra parameters” (no constrained-decoding grammar keys documented)
  - `stream`, `stream_options` for streaming

## Grammar dialect and caveats
- **Dialect documented:** JSON Schema (via `response_format.type="json_schema"`), with schema expected to be JSON-Schema-compliant.
- **Caveat/inconsistency:** one official page documents `json_schema`, but chat-completions API reference currently says only `json_object` or `text` for `response_format`.
- **Inference:** Nebius clearly supports JSON-structured output; official docs do **not** clearly advertise CFG/regex grammar decoding primitives.

## Streaming fields
- Request-side streaming controls:
  - `stream: true`
  - `stream_options: {"include_usage": true}` (usage included in final chunk)
- Response-side streaming docs state:
  - data-only SSE chunks
  - stream ends with `data: [DONE]`
  - response schema lists `ChatCompletionChunk` as a response type, but chunk field-level schema is not clearly expanded on-page.

## Sources (URLs)
- https://docs.tokenfactory.nebius.com/api-reference/inference/create-chat-completion
- https://docs.tokenfactory.nebius.com/ai-models-inference/json
- https://docs.tokenfactory.nebius.com/ai-models-inference/overview
- https://docs.tokenfactory.nebius.com/api-reference/models/list-models
- https://docs.tokenfactory.nebius.com/api-reference/examples/list-of-models

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
session id: 019c5b0e-4762-75c1-b6a7-713ce89707a2
--------
user
Research official documentation for provider "Nebius" focused on grammar-constrained generation.
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
2026-02-14T07:29:48.411878Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5531-6c60-7612-b81c-b02333263b22
2026-02-14T07:29:48.432556Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5080-050b-7c53-92a8-9c52ce325359
2026-02-14T07:29:48.453224Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c58f2-9999-7e13-8897-cb3cb6765c62
2026-02-14T07:29:48.473856Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5ae2-4d18-7921-a6f9-9ca09a337133
2026-02-14T07:29:48.494576Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-1e63-7422-8df1-29cc3cd854ed
2026-02-14T07:29:48.515355Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-2af1-7321-8d40-367f5a3ba03a
2026-02-14T07:29:48.535953Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-8eca-7cf3-8c60-d66e26ea0144
2026-02-14T07:29:48.556745Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-1935-7772-bf75-7eb9d084599e
2026-02-14T07:29:48.577523Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-45eb-7810-9be4-e9c813827907
2026-02-14T07:29:48.598311Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-5630-7b30-8723-45187528edea
2026-02-14T07:29:48.618927Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0a-f457-71d1-902a-d41b0df6fafa
2026-02-14T07:29:48.639655Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0a-f500-7013-80bc-cc4e70470657
2026-02-14T07:29:48.660237Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-1200-74e2-b68a-b5695adf8ddc
2026-02-14T07:29:48.681040Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-4f6c-79a1-ad3e-23dd8a997ea2
2026-02-14T07:29:48.702376Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e2-75e1-99f8-269a75536055
2026-02-14T07:29:48.723143Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e0-7850-aab6-44bd39f1876c
2026-02-14T07:29:48.743934Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e3-7490-b15b-7731fbbd70ff
2026-02-14T07:29:48.764858Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-fd96-7c40-9fb5-4533f503a218
2026-02-14T07:29:48.785939Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0d-db4c-7cc2-99b4-a433007462d2
2026-02-14T07:29:48.806623Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0d-f250-71f3-b5b4-0ea37af65fb7
2026-02-14T07:29:48.827363Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0d-f508-7283-bcc5-b2effda3a024
2026-02-14T07:29:48.848119Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0e-2f50-7813-ba50-182d396da368
mcp: surrealdb ready
mcp: playwright ready
mcp: exa ready
mcp startup: ready: surrealdb, playwright, exa

thinking
**Planning official docs lookup**
codex
I’ll check Nebius’s official API/docs for constrained decoding details (grammar/CFG/regex), then extract exact request and streaming fields with source links.
🌐 Searching the web...
🌐 Searched: Nebius AI Studio documentation grammar constrained decoding regex CFG streaming fields

thinking
**Planning query-specific API reference**
🌐 Searching the web...
🌐 Searched: site:docs.studio.nebius.com vLLM parameters guided_json guided_regex guided_grammar Nebius

thinking
**Planning webpage opening with extras**
codex
I found the key Nebius pages (`create-chat-completion` and `structured output & JSON`) and I’m now pulling exact field names plus any constrained-decoding specifics and streaming chunk fields.
🌐 Searching the web...
🌐 Searched: https://docs.studio.nebius.com/api-reference/inference/create-chat-completion

thinking
**Preparing content lines extraction**
🌐 Searching the web...
🌐 Searched: 'guided' in https://docs.studio.nebius.com/ai-models-inference/json

thinking
**Identifying streaming response usage**
🌐 Searching the web...
🌐 Searched: site:docs.tokenfactory.nebius.com chat.completion.chunk choices delta role content

thinking
**Confirming streaming response format**
codex
I confirmed Nebius documents JSON schema output but I still need one source that explicitly shows streaming chunk structure; I’m searching for a Nebius chat-stream example rather than inferring from OpenAI defaults.
🌐 Searching the web...
🌐 Searched: site:docs.tokenfactory.nebius.com "for chunk in client.chat.completions.create" stream=True

thinking
**Inspecting response schema structure**
🌐 Searching the web...
🌐 Searched: https://docs.studio.nebius.com/api-reference/inference/create-chat-completion

thinking
**Evaluating navigation for chunk details**
codex
I found that the endpoint schema explicitly lists `ChatCompletionResponse` and `ChatCompletionChunk` as response types and documents SSE behavior; next I’ll verify if Nebius exposes any explicit `guided_regex`/`guided_grammar` parameters in official docs.
🌐 Searching the web...
🌐 Searched: site:docs.tokenfactory.nebius.com "ChatCompletionChunk"

thinking
**Checking OpenAPI spec availability**
🌐 Searching the web...
🌐 Searched: site:docs.tokenfactory.nebius.com openapi.json tokenfactory

thinking
**Verifying full parameter support**
🌐 Searching the web...
🌐 Searched: https://docs.studio.nebius.com/ai-models-inference/inference

thinking
**Identifying navigation link necessity**
🌐 Searching the web...
🌐 Searched: https://docs.studio.nebius.com/ai-models-inference/overview
codex
I found a key line: Nebius API supports the full set of vLLM parameters. I’ll inspect the linked “additional model parameters” section to confirm whether they document guided grammar/regex fields by name.
🌐 Searching the web...
🌐 Searched: https://docs.tokenfactory.nebius.com/api-reference/examples/list-of-models

thinking
**Locating RichModel schema source**
🌐 Searching the web...
🌐 Searched: https://docs.tokenfactory.nebius.com/api-reference/models/list-models

thinking
**Exploring endpoint options**
🌐 Searching the web...
🌐 Searched: https://docs.tokenfactory.nebius.com/api-reference/inference/generate

thinking
**Highlighting documentation inconsistencies**
codex
## Provider
Nebius (currently branded in docs as **Nebius Token Factory**, OpenAI-compatible API at `https://api.tokenfactory.nebius.com/v1`).

## Grammar capability
- **Documented support:** structured JSON output via `response_format`.
- **Not explicitly documented:** CFG grammar constraints, regex-constrained decoding, or EBNF/GBNF-style grammar fields.
- I found no official Nebius doc fields named like `guided_regex`, `guided_grammar`, `grammar`, or `regex` in chat/completions docs.

## Request shape
- Main endpoint: `POST /v1/chat/completions`
- Relevant fields:
  - `response_format` (documented values vary by page):
    - Structured output page: `{"type":"json_schema","json_schema":...}` and `{"type":"json_object"}`
    - API reference page for chat completions: says only `{'type':'json_object'}` or `{'type':'text'}`
  - `extra_body`: generic object “to provide extra parameters” (no constrained-decoding grammar keys documented)
  - `stream`, `stream_options` for streaming

## Grammar dialect and caveats
- **Dialect documented:** JSON Schema (via `response_format.type="json_schema"`), with schema expected to be JSON-Schema-compliant.
- **Caveat/inconsistency:** one official page documents `json_schema`, but chat-completions API reference currently says only `json_object` or `text` for `response_format`.
- **Inference:** Nebius clearly supports JSON-structured output; official docs do **not** clearly advertise CFG/regex grammar decoding primitives.

## Streaming fields
- Request-side streaming controls:
  - `stream: true`
  - `stream_options: {"include_usage": true}` (usage included in final chunk)
- Response-side streaming docs state:
  - data-only SSE chunks
  - stream ends with `data: [DONE]`
  - response schema lists `ChatCompletionChunk` as a response type, but chunk field-level schema is not clearly expanded on-page.

## Sources (URLs)
- https://docs.tokenfactory.nebius.com/api-reference/inference/create-chat-completion
- https://docs.tokenfactory.nebius.com/ai-models-inference/json
- https://docs.tokenfactory.nebius.com/ai-models-inference/overview
- https://docs.tokenfactory.nebius.com/api-reference/models/list-models
- https://docs.tokenfactory.nebius.com/api-reference/examples/list-of-models
tokens used
41,994
```

