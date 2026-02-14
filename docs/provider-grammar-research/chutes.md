## Provider
**Chutes** (`chutes.ai`) offers OpenAI-compatible LLM endpoints via template backends (notably **vLLM** and **SGLang**) on deployed chutes.

## Grammar capability
- **Documented as supported (vLLM template):**
  - Guided constrained decoding via `guided_decoding_backend` and request-time `guided_json`.
- **Documented as supported (SGLang template):**
  - Regex-constrained token generation in SGLang programs (`sglang.gen(..., regex=...)`).
- **Not explicitly documented in Chutes docs as request-level support:**
  - CFG grammar fields (no explicit `guided_grammar`/CFG request examples in Chutes docs).
  - Regex-constrained decoding as an OpenAI `/v1/chat/completions` request field (only shown in SGLang program code, not OpenAI request schema).

## Request shape
- OpenAI-compatible endpoint on vLLM chutes: `POST /v1/chat/completions`
- Standard fields shown: `model`, `messages`, `max_tokens`, `temperature`, `stream`
- Constrained-output field shown in Chutes docs:
  - `guided_json: { ...JSON schema/object... }`
- Backend enablement shown at deployment/config level:
  - `engine_args: { "guided_decoding_backend": "outlines" }`

## Grammar dialect and caveats
- **Dialect documented directly by Chutes:** JSON-guided decoding via `guided_json` (schema-like object).
- **Regex constraints:** shown in SGLang function API (`regex=...`) rather than OpenAI request body.
- **Caveat:** Chutes docs do not provide a full formal list of grammar/CFG/regex request fields for `/v1/chat/completions`; support appears backend-dependent (vLLM vs SGLang) and may vary by chute configuration.

## Streaming fields
For OpenAI-compatible streaming examples in Chutes vLLM docs:
- Request uses `stream: true`
- SSE chunks parsed from `data: ...`
- Response chunks use OpenAI-style structure with:
  - `choices[0].delta.content` (token/text deltas)

## Sources (URLs)
- https://chutes.ai/docs/templates/vllm
- https://chutes.ai/docs/templates/sglang
- https://chutes.ai/docs/examples/llm-chat
- https://chutes.ai/docs/integrations/vercel-ai-sdk

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
session id: 019c5b0c-fd87-77a2-b52d-3b01e53fde37
--------
user
Research official documentation for provider "Chutes" focused on grammar-constrained generation.
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
2026-02-14T07:28:23.978316Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5531-6c60-7612-b81c-b02333263b22
2026-02-14T07:28:24.007898Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5080-050b-7c53-92a8-9c52ce325359
2026-02-14T07:28:24.032554Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c58f2-9999-7e13-8897-cb3cb6765c62
2026-02-14T07:28:24.047506Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5ae2-4d18-7921-a6f9-9ca09a337133
2026-02-14T07:28:24.063221Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-1e63-7422-8df1-29cc3cd854ed
2026-02-14T07:28:24.080751Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-2af1-7321-8d40-367f5a3ba03a
2026-02-14T07:28:24.107529Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-8eca-7cf3-8c60-d66e26ea0144
2026-02-14T07:28:24.136407Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-1935-7772-bf75-7eb9d084599e
2026-02-14T07:28:24.170891Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-45eb-7810-9be4-e9c813827907
2026-02-14T07:28:24.184989Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-5630-7b30-8723-45187528edea
2026-02-14T07:28:24.217754Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0a-f457-71d1-902a-d41b0df6fafa
2026-02-14T07:28:24.247115Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0a-f500-7013-80bc-cc4e70470657
2026-02-14T07:28:24.272908Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-1200-74e2-b68a-b5695adf8ddc
2026-02-14T07:28:24.307737Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-4f6c-79a1-ad3e-23dd8a997ea2
2026-02-14T07:28:24.338893Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e2-75e1-99f8-269a75536055
2026-02-14T07:28:24.369618Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e0-7850-aab6-44bd39f1876c
2026-02-14T07:28:24.387551Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e3-7490-b15b-7731fbbd70ff
mcp: surrealdb ready
mcp: playwright ready
mcp: exa ready
mcp startup: ready: surrealdb, playwright, exa

thinking
**Preparing web search for docs**
🌐 Searching the web...
🌐 Searched: Chutes API documentation grammar constrained generation CFG regex constrained decoding

thinking
**Considering domain-restricted search**
🌐 Searching the web...
🌐 Searched: site:docs.chutes.ai grammar constrained decoding

thinking
**Exploring website for documentation links**
🌐 Searching the web...
🌐 Searched: https://npm-demo.chutes.ai/

thinking
**Exploring SDK repo for structured output support**
🌐 Searching the web...
🌐 Searched: https://github.com/chutesai/ai-sdk-provider-chutes

thinking
**Searching repo for grammar rules**
🌐 Searching the web...
🌐 Searched: 'grammar' in https://github.com/chutesai/ai-sdk-provider-chutes

thinking
**Researching official grammar API docs**
🌐 Searching the web...
🌐 Searched: site:chutes.ai "response_format" "chat/completions"
🌐 Searching the web...
🌐 Searched: https://chutes.ai/

thinking
**Identifying docs link parameters**
🌐 Searching the web...
🌐 Searched: https://chutes.ai/resources

thinking
**Exploring documentation access options**
🌐 Searching the web...
🌐 Searched: https://docs.chutes.ai/

thinking
**Exploring Vercel AI SDK integration**
🌐 Searching the web...
🌐 Searched: https://chutes.ai/docs/integrations/vercel-ai-sdk
🌐 Searching the web...
🌐 Searched: 'structured generation' in https://chutes.ai/docs/examples/llm-chat

thinking
**Checking structured output fields**
🌐 Searching the web...
🌐 Searched: https://chutes.ai/docs/templates/sglang

thinking
**Reviewing API request field requirements**
🌐 Searching the web...
🌐 Searched: https://chutes.ai/docs/api-reference/invocations

thinking
**Inspecting template for guided params**
🌐 Searching the web...
🌐 Searched: 'guided' in https://chutes.ai/docs/templates/vllm

thinking
**Checking guided generation docs**
🌐 Searching the web...
🌐 Searched: https://chutes.ai/docs/templates/vllm

thinking
**Assessing Chutes API request fields**
🌐 Searching the web...
🌐 Searched: 'data: ' in https://chutes.ai/docs/guides/streaming

thinking
**Verifying guided_json schema usage**
🌐 Searching the web...
🌐 Searched: site:chutes.ai/docs "guided_json"

thinking
**Verifying supported decoding constraints**
codex
## Provider
**Chutes** (`chutes.ai`) offers OpenAI-compatible LLM endpoints via template backends (notably **vLLM** and **SGLang**) on deployed chutes.

## Grammar capability
- **Documented as supported (vLLM template):**
  - Guided constrained decoding via `guided_decoding_backend` and request-time `guided_json`.
- **Documented as supported (SGLang template):**
  - Regex-constrained token generation in SGLang programs (`sglang.gen(..., regex=...)`).
- **Not explicitly documented in Chutes docs as request-level support:**
  - CFG grammar fields (no explicit `guided_grammar`/CFG request examples in Chutes docs).
  - Regex-constrained decoding as an OpenAI `/v1/chat/completions` request field (only shown in SGLang program code, not OpenAI request schema).

## Request shape
- OpenAI-compatible endpoint on vLLM chutes: `POST /v1/chat/completions`
- Standard fields shown: `model`, `messages`, `max_tokens`, `temperature`, `stream`
- Constrained-output field shown in Chutes docs:
  - `guided_json: { ...JSON schema/object... }`
- Backend enablement shown at deployment/config level:
  - `engine_args: { "guided_decoding_backend": "outlines" }`

## Grammar dialect and caveats
- **Dialect documented directly by Chutes:** JSON-guided decoding via `guided_json` (schema-like object).
- **Regex constraints:** shown in SGLang function API (`regex=...`) rather than OpenAI request body.
- **Caveat:** Chutes docs do not provide a full formal list of grammar/CFG/regex request fields for `/v1/chat/completions`; support appears backend-dependent (vLLM vs SGLang) and may vary by chute configuration.

## Streaming fields
For OpenAI-compatible streaming examples in Chutes vLLM docs:
- Request uses `stream: true`
- SSE chunks parsed from `data: ...`
- Response chunks use OpenAI-style structure with:
  - `choices[0].delta.content` (token/text deltas)

## Sources (URLs)
- https://chutes.ai/docs/templates/vllm
- https://chutes.ai/docs/templates/sglang
- https://chutes.ai/docs/examples/llm-chat
- https://chutes.ai/docs/integrations/vercel-ai-sdk
tokens used
62,385
```

