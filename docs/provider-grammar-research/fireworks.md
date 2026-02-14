## Provider
**Fireworks AI** (`https://api.fireworks.ai/inference/v1`), OpenAI-compatible `POST /chat/completions`.

## Grammar capability
- Supports constrained decoding via **Grammar mode** in structured outputs.
- Fireworks docs describe it as forcing output schema with **extended BNF (GBNF)**.
- Docs state grammar mode is supported for “all Fireworks models” (in their grammar guide example context).

## Request shape
Use `response_format` on chat completions:
```json
{
  "model": "accounts/fireworks/models/...",
  "messages": [...],
  "response_format": {
    "type": "grammar",
    "grammar": "root ::= ..."
  },
  "stream": true
}
```
Also documented in API schema:
- `response_format.type`
- `response_format.grammar`
- other modes: `json_object`, `json_schema`.

## Grammar dialect and caveats
- Dialect: **GBNF / extended BNF**, inspired by `llama.cpp`.
- Syntax includes BNF rules plus “modern regex-like features” (character classes/ranges, repetition, optionals).
- No separate documented `response_format.type: "regex"` mode; regex-like constraints are expressed inside grammar rules.
- Caveat from docs: prompt engineering is still recommended for best results.

## Streaming fields
From Fireworks chat-completions docs + SDK reference:
- Streaming is SSE; stream ends with `data: [DONE]`.
- Stream chunks expose choice deltas:
  - `choices[].delta.role`
  - `choices[].delta.content`
  - `choices[].finish_reason`
- Top-level stream metadata includes `id`, `object`, `created`, `model`, `choices`.

## Sources (URLs)
- https://docs.fireworks.ai/structured-responses/structured-output-grammar-based
- https://docs.fireworks.ai/structured-responses/structured-response-formatting
- https://docs.fireworks.ai/api-reference/post-chatcompletions
- https://docs.fireworks.ai/tools-sdks/python-client/api-reference

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
session id: 019c5b0c-fd87-7052-8ac2-b00d4441b34b
--------
user
Research official documentation for provider "Fireworks" focused on grammar-constrained generation.
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
mcp: exa starting
mcp: surrealdb starting
2026-02-14T07:28:23.983578Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5531-6c60-7612-b81c-b02333263b22
2026-02-14T07:28:24.016650Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5080-050b-7c53-92a8-9c52ce325359
2026-02-14T07:28:24.050890Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c58f2-9999-7e13-8897-cb3cb6765c62
2026-02-14T07:28:24.074872Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5ae2-4d18-7921-a6f9-9ca09a337133
2026-02-14T07:28:24.109923Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-1e63-7422-8df1-29cc3cd854ed
2026-02-14T07:28:24.127550Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-2af1-7321-8d40-367f5a3ba03a
2026-02-14T07:28:24.149014Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-8eca-7cf3-8c60-d66e26ea0144
2026-02-14T07:28:24.186791Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-1935-7772-bf75-7eb9d084599e
2026-02-14T07:28:24.221882Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-45eb-7810-9be4-e9c813827907
2026-02-14T07:28:24.246721Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-5630-7b30-8723-45187528edea
2026-02-14T07:28:24.279171Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0a-f457-71d1-902a-d41b0df6fafa
2026-02-14T07:28:24.313136Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0a-f500-7013-80bc-cc4e70470657
2026-02-14T07:28:24.329227Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-1200-74e2-b68a-b5695adf8ddc
2026-02-14T07:28:24.359227Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-4f6c-79a1-ad3e-23dd8a997ea2
2026-02-14T07:28:24.385887Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e2-75e1-99f8-269a75536055
2026-02-14T07:28:24.402411Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e0-7850-aab6-44bd39f1876c
2026-02-14T07:28:24.427276Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e3-7490-b15b-7731fbbd70ff
mcp: surrealdb ready
mcp: playwright ready
mcp: exa ready
mcp startup: ready: surrealdb, playwright, exa
codex
I’ll check Fireworks’ official docs for constrained decoding details (grammar/CFG/regex), then extract exact request and streaming fields with source links.
🌐 Searching the web...
🌐 Searched: Fireworks AI grammar constrained decoding documentation

thinking
**Searching API response format details**
codex
I found the structured output docs and will now verify exact API fields from Fireworks’ API reference, including streaming chunk structure.
🌐 Searching the web...
🌐 Searched: site:docs.fireworks.ai api-reference post-chat-completions response_format grammar

thinking
**Exploring streaming options**
🌐 Searching the web...
🌐 Searched: https://docs.fireworks.ai/api-reference/post-chatcompletions

thinking
**Identifying streaming response pattern**
🌐 Searching the web...
🌐 Searched: 'chat.completion.chunk' in https://docs.fireworks.ai/api-reference/post-chatcompletions

thinking
**Checking streaming response and grammar syntax**
codex
I’ve confirmed `response_format` and SSE behavior on the chat-completions endpoint; next I’m checking the grammar syntax section for dialect details (including any regex support).
🌐 Searching the web...
🌐 Searched: https://docs.fireworks.ai/structured-responses/structured-output-grammar-based

thinking
**Separating find and open calls**
🌐 Searching the web...
🌐 Searched: 'Syntax' in https://docs.fireworks.ai/structured-responses/structured-output-grammar-based

thinking
**Confirming streaming field details**
🌐 Searching the web...
🌐 Searched: https://docs.fireworks.ai/tools-sdks/python-client/api-reference

thinking
**Confirming no regex mode**
codex
## Provider
**Fireworks AI** (`https://api.fireworks.ai/inference/v1`), OpenAI-compatible `POST /chat/completions`.

## Grammar capability
- Supports constrained decoding via **Grammar mode** in structured outputs.
- Fireworks docs describe it as forcing output schema with **extended BNF (GBNF)**.
- Docs state grammar mode is supported for “all Fireworks models” (in their grammar guide example context).

## Request shape
Use `response_format` on chat completions:
```json
{
  "model": "accounts/fireworks/models/...",
  "messages": [...],
  "response_format": {
    "type": "grammar",
    "grammar": "root ::= ..."
  },
  "stream": true
}
```
Also documented in API schema:
- `response_format.type`
- `response_format.grammar`
- other modes: `json_object`, `json_schema`.

## Grammar dialect and caveats
- Dialect: **GBNF / extended BNF**, inspired by `llama.cpp`.
- Syntax includes BNF rules plus “modern regex-like features” (character classes/ranges, repetition, optionals).
- No separate documented `response_format.type: "regex"` mode; regex-like constraints are expressed inside grammar rules.
- Caveat from docs: prompt engineering is still recommended for best results.

## Streaming fields
From Fireworks chat-completions docs + SDK reference:
- Streaming is SSE; stream ends with `data: [DONE]`.
- Stream chunks expose choice deltas:
  - `choices[].delta.role`
  - `choices[].delta.content`
  - `choices[].finish_reason`
- Top-level stream metadata includes `id`, `object`, `created`, `model`, `choices`.

## Sources (URLs)
- https://docs.fireworks.ai/structured-responses/structured-output-grammar-based
- https://docs.fireworks.ai/structured-responses/structured-response-formatting
- https://docs.fireworks.ai/api-reference/post-chatcompletions
- https://docs.fireworks.ai/tools-sdks/python-client/api-reference
tokens used
30,738
```

