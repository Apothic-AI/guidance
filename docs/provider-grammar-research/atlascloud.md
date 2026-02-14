## Provider
**Atlas Cloud** (`api.atlascloud.ai`) with docs at `atlascloud.ai/docs` (plus legacy docs at `docs.atlascloud.ai`).

## Grammar capability
As of **2026-02-14**, Atlas Cloud’s official chat-completions docs do **not** document grammar-constrained decoding features (no CFG/BNF/GBNF/regex/JSON-schema constrained decoding fields shown).

## Request shape
Documented `POST /api/v1/chat/completions` request fields:
- `model` (string)
- `messages` (array)
- `max_tokens` (integer, optional)
- `temperature` (number, optional)
- `top_p` (number, optional)
- `top_k` (integer, optional)
- `repetition_penalty` (number, optional)
- `stream` (boolean, optional)
- `systemPrompt` (string, optional)
- `thinking` (object, optional)

## Grammar dialect and caveats
No grammar dialect is specified in official docs (no regex dialect, no CFG format, no grammar schema format documented).  
Caveat: Atlas says its API is OpenAI-`ChatCompletion` compatible, but their documented request schema currently omits OpenAI-style structured-output fields such as `response_format`/`json_schema`.

## Streaming fields
Documented streaming-related info:
- Request flag: `stream: boolean`
- Behavior note: “partial message deltas will be sent as server-sent events”
- No explicit streamed chunk schema/field list is documented on the endpoint page (e.g., no documented `choices[].delta` structure on that page).

## Sources (URLs)
- https://www.atlascloud.ai/docs/createChatCompletion  
- https://www.atlascloud.ai/docs/models/llm  
- https://docs.atlascloud.ai/playground/

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
session id: 019c5b0c-fd89-7162-9102-1207ec15728d
--------
user
Research official documentation for provider "AtlasCloud" focused on grammar-constrained generation.
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
2026-02-14T07:28:23.993758Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5531-6c60-7612-b81c-b02333263b22
2026-02-14T07:28:24.028648Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5080-050b-7c53-92a8-9c52ce325359
2026-02-14T07:28:24.065608Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c58f2-9999-7e13-8897-cb3cb6765c62
2026-02-14T07:28:24.094846Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5ae2-4d18-7921-a6f9-9ca09a337133
2026-02-14T07:28:24.118776Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-1e63-7422-8df1-29cc3cd854ed
2026-02-14T07:28:24.135003Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-2af1-7321-8d40-367f5a3ba03a
2026-02-14T07:28:24.150969Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-8eca-7cf3-8c60-d66e26ea0144
2026-02-14T07:28:24.180522Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-1935-7772-bf75-7eb9d084599e
2026-02-14T07:28:24.194775Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-45eb-7810-9be4-e9c813827907
2026-02-14T07:28:24.228228Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-5630-7b30-8723-45187528edea
2026-02-14T07:28:24.255035Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0a-f457-71d1-902a-d41b0df6fafa
2026-02-14T07:28:24.283950Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0a-f500-7013-80bc-cc4e70470657
2026-02-14T07:28:24.313932Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-1200-74e2-b68a-b5695adf8ddc
2026-02-14T07:28:24.342003Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-4f6c-79a1-ad3e-23dd8a997ea2
2026-02-14T07:28:24.370315Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e2-75e1-99f8-269a75536055
2026-02-14T07:28:24.393238Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e0-7850-aab6-44bd39f1876c
2026-02-14T07:28:24.406266Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e3-7490-b15b-7731fbbd70ff
mcp: surrealdb ready
mcp: playwright ready
mcp: exa ready
mcp startup: ready: surrealdb, playwright, exa

thinking
**Initiating web search on provider**
codex
I’ll look up AtlasCloud’s official docs and extract only constrained-generation details: support status, request fields, grammar dialect, and streaming fields. I’m starting with targeted searches and then validating against primary documentation pages.
🌐 Searching the web...
🌐 Searched: AtlasCloud official documentation grammar constrained decoding CFG regex streaming API

thinking
**Refining search scope to specific domains**
codex
Search results are noisy so far and not showing a clear official AtlasCloud API source. I’m now probing likely official domains and API-reference pages directly to confirm whether this provider exists and exposes constrained decoding fields.
🌐 Searching the web...
🌐 Searched: AtlasCloud API documentation

thinking
**Exploring docs for AI endpoints**
codex
I found the likely correct provider docs at `atlascloud.ai` (API host `api.atlascloud.ai`) and am now drilling into their text-generation endpoints to verify if grammar/regex/CFG constraints exist or not.
🌐 Searching the web...
🌐 Searched: https://www.atlascloud.ai/docs/es/more-models/atlascloud/image-background-remover/generateImage
🌐 Searching the web...
🌐 Searched: https://www.atlascloud.ai/docs/es/createChatCompletion

thinking
**Checking model compatibility**
codex
I located the core chat endpoint docs (`/api/v1/chat/completions`) and the listed request fields; next I’m checking model/guide pages for any hidden `response_format`, grammar, regex, or JSON-schema constraint parameters not shown in the endpoint table.
🌐 Searching the web...
🌐 Searched: https://www.atlascloud.ai/docs/es/models/llm

thinking
**Exploring English docs for SSE info**
codex
The LLM docs currently show OpenAI-style chat completions plus `stream: boolean`, but no grammar-related fields so far. I’ll check the English variant and any OpenAPI spec exports to confirm this is truly unsupported rather than undocumented in one locale.
🌐 Searching the web...
🌐 Searched: site:atlascloud.ai/docs createChatCompletion response_format json_schema

thinking
**Exploring page structure for attributes**
🌐 Searching the web...
🌐 Searched: https://www.atlascloud.ai/docs/createChatCompletion

thinking
**Separating find operation from open call**
codex
I confirmed the English API page mirrors the same fields. I’m doing one more pass across Atlas docs/search for explicit mentions of `response_format`, JSON schema, grammar, or regex to avoid false negatives.
🌐 Searching the web...
🌐 Searched: 'response_format' in https://www.atlascloud.ai/docs/createChatCompletion

thinking
**Investigating attribute reveal trigger**
🌐 Searching the web...
🌐 Searched: https://www.atlascloud.ai/docs/createChatCompletion

thinking
**Checking streaming response schema**
codex
I can’t see any explicit schema for streamed chunks on the docs page itself, only a statement that SSE deltas are emitted. I’ll do a quick check for a published OpenAPI JSON/YAML on AtlasCloud to see if chunk field names are documented there.
🌐 Searching the web...
🌐 Searched: site:atlascloud.ai openapi.json atlascloud api

thinking
**Planning concise API markdown**
codex
## Provider
**Atlas Cloud** (`api.atlascloud.ai`) with docs at `atlascloud.ai/docs` (plus legacy docs at `docs.atlascloud.ai`).

## Grammar capability
As of **2026-02-14**, Atlas Cloud’s official chat-completions docs do **not** document grammar-constrained decoding features (no CFG/BNF/GBNF/regex/JSON-schema constrained decoding fields shown).

## Request shape
Documented `POST /api/v1/chat/completions` request fields:
- `model` (string)
- `messages` (array)
- `max_tokens` (integer, optional)
- `temperature` (number, optional)
- `top_p` (number, optional)
- `top_k` (integer, optional)
- `repetition_penalty` (number, optional)
- `stream` (boolean, optional)
- `systemPrompt` (string, optional)
- `thinking` (object, optional)

## Grammar dialect and caveats
No grammar dialect is specified in official docs (no regex dialect, no CFG format, no grammar schema format documented).  
Caveat: Atlas says its API is OpenAI-`ChatCompletion` compatible, but their documented request schema currently omits OpenAI-style structured-output fields such as `response_format`/`json_schema`.

## Streaming fields
Documented streaming-related info:
- Request flag: `stream: boolean`
- Behavior note: “partial message deltas will be sent as server-sent events”
- No explicit streamed chunk schema/field list is documented on the endpoint page (e.g., no documented `choices[].delta` structure on that page).

## Sources (URLs)
- https://www.atlascloud.ai/docs/createChatCompletion  
- https://www.atlascloud.ai/docs/models/llm  
- https://docs.atlascloud.ai/playground/
tokens used
28,676
```

