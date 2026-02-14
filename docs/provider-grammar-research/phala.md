### Provider
**Phala (Confidential AI via RedPill OpenAI-compatible API)**  
Documented endpoint: `POST https://api.redpill.ai/v1/chat/completions` (Phala docs use this in Structured Output and On-demand API pages).

### Grammar capability
- **Documented:** structured output via JSON schema (`response_format`).
- **Not documented:** explicit **grammar/CFG/regex constrained decoding** fields or APIs.

### Request shape
From Phala Structured Output docs, request includes:
- `model`
- `messages`
- `response_format`:
  - `type: "json_schema"`
  - `json_schema.name`
  - `json_schema.strict`
  - `json_schema.schema` (JSON Schema object)

### Grammar dialect and caveats
- **Dialect:** appears to be **OpenAI-style `json_schema` structured output** (JSON Schema-based), not a published CFG/regex grammar DSL.
- **Caveats (documented):**
  - Structured output is listed as supported only for specific Phala models on that page.
  - No published spec for supported JSON Schema subset/limits (so treat unsupported keywords/features as unspecified).
  - Phala docs show a base URL inconsistency on Streaming page (`/api/v1`) vs other pages (`/v1`); structured-output examples use `/v1`.

### Streaming fields
For streamed output (SSE), documented chunks include:
- `choices[].delta.content`
- stream terminator: `data: [DONE]`
- No Phala-specific extra streaming fields for constrained output are documented (e.g., no grammar state/validator fields).

### Sources (URLs)
- https://docs.phala.com/phala-cloud/confidential-ai/confidential-model/structured-output
- https://docs.phala.com/phala-cloud/confidential-ai/confidential-model/streaming
- https://docs.phala.com/phala-cloud/confidential-ai/confidential-model/confidential-ai-api
- https://docs.redpill.ai/developers/api-reference/chat-completions
- https://docs.redpill.ai/developers/guides/streaming

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
session id: 019c5b0e-b66a-79c1-a388-4af5a76df995
--------
user
Research official documentation for provider "Phala" focused on grammar-constrained generation.
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
2026-02-14T07:30:16.840114Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5531-6c60-7612-b81c-b02333263b22
2026-02-14T07:30:16.860900Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5080-050b-7c53-92a8-9c52ce325359
2026-02-14T07:30:16.881648Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c58f2-9999-7e13-8897-cb3cb6765c62
2026-02-14T07:30:16.902509Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5ae2-4d18-7921-a6f9-9ca09a337133
2026-02-14T07:30:16.923358Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-1e63-7422-8df1-29cc3cd854ed
2026-02-14T07:30:16.944255Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-2af1-7321-8d40-367f5a3ba03a
2026-02-14T07:30:16.964970Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-8eca-7cf3-8c60-d66e26ea0144
2026-02-14T07:30:16.985731Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-1935-7772-bf75-7eb9d084599e
2026-02-14T07:30:17.006570Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-45eb-7810-9be4-e9c813827907
2026-02-14T07:30:17.027315Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-5630-7b30-8723-45187528edea
2026-02-14T07:30:17.048047Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0a-f457-71d1-902a-d41b0df6fafa
2026-02-14T07:30:17.068906Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0a-f500-7013-80bc-cc4e70470657
2026-02-14T07:30:17.089713Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-1200-74e2-b68a-b5695adf8ddc
2026-02-14T07:30:17.110493Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-4f6c-79a1-ad3e-23dd8a997ea2
2026-02-14T07:30:17.131255Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e2-75e1-99f8-269a75536055
2026-02-14T07:30:17.152085Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e0-7850-aab6-44bd39f1876c
2026-02-14T07:30:17.172899Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e3-7490-b15b-7731fbbd70ff
2026-02-14T07:30:17.193845Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0e-2f50-7813-ba50-182d396da368
2026-02-14T07:30:17.214721Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0e-4762-75c1-b6a7-713ce89707a2
2026-02-14T07:30:17.235688Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0e-4ff4-7c11-809c-677b76971da0
2026-02-14T07:30:17.256487Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0e-7fe1-7683-ad3b-c244133d6497
2026-02-14T07:30:17.277452Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0e-b4b5-7fe2-a3e5-58d9a3aefdc9
mcp: surrealdb ready
mcp: playwright ready
mcp: exa ready
mcp startup: ready: surrealdb, playwright, exa

thinking
**Planning official docs search**
codex
I’ll check Phala’s official docs directly and extract only constraint-related details: whether grammar/CFG/regex decoding is supported, the exact request fields, dialect notes, and streaming response fields. I’m starting with targeted source discovery now.
🌐 Searching the web...
🌐 Searched: Phala official documentation grammar constrained generation CFG regex decoding

thinking
**Checking official API docs**
codex
I found Phala’s official API docs and I’m now checking whether they document any constraint-specific fields beyond generic OpenAI compatibility. I’ll verify this against their API reference pages next.
🌐 Searching the web...
🌐 Searched: https://docs.phala.com/phala-cloud/confidential-ai/confidential-model/confidential-ai-api

thinking
**Examining structured output and streaming fields**
🌐 Searching the web...
🌐 Searched: https://docs.phala.com/phala-cloud/confidential-ai/confidential-model/structured-output

thinking
**Checking Phala docs for grammar constraints**
codex
I confirmed the Phala pages for `Structured Output` and `Streaming`. Next I’m checking the rest of official docs for any mention of `grammar`, `cfg`, `regex`, or guided decoding fields so we can distinguish documented support vs inference.
🌐 Searching the web...
🌐 Searched: site:docs.phala.com grammar constrained decoding

thinking
**Researching grammar constraint docs**
codex
I didn’t find `grammar/cfg/regex` mentions on Phala docs search results yet. I’m now checking Redpill API docs (the official endpoint Phala uses) to see if constrained decoding is documented there instead.
🌐 Searching the web...
🌐 Searched: site:redpill.ai/docs guided decoding regex grammar cfg

thinking
**Identifying create-chat-completion details**
🌐 Searching the web...
🌐 Searched: https://docs.redpill.ai/get-started/api-reference/create-chat-completion

thinking
**Identifying official API docs source**
🌐 Searching the web...
🌐 Searched: site:docs.redpill.ai developers api reference chat completions response_format json_schema

thinking
**Locating chat completions docs**
🌐 Searching the web...
🌐 Searched: https://docs.redpill.ai/developers/api-reference/overview

thinking
**Linking ID to chat completions**
🌐 Searching the web...
🌐 Searched: https://docs.redpill.ai/api-reference/chat-completions

thinking
**Identifying broken links due to site restructure**
🌐 Searching the web...
🌐 Searched: https://docs.redpill.ai/developers/api-reference/chat-completions
🌐 Searching the web...
🌐 Searched: https://docs.redpill.ai/developers/guides/streaming

thinking
**Checking response format usage**
🌐 Searching the web...
🌐 Searched: 'response_format' in https://docs.redpill.ai/developers/api-reference/chat-completions

thinking
**Synthesizing structured output details**
codex
### Provider
**Phala (Confidential AI via RedPill OpenAI-compatible API)**  
Documented endpoint: `POST https://api.redpill.ai/v1/chat/completions` (Phala docs use this in Structured Output and On-demand API pages).

### Grammar capability
- **Documented:** structured output via JSON schema (`response_format`).
- **Not documented:** explicit **grammar/CFG/regex constrained decoding** fields or APIs.

### Request shape
From Phala Structured Output docs, request includes:
- `model`
- `messages`
- `response_format`:
  - `type: "json_schema"`
  - `json_schema.name`
  - `json_schema.strict`
  - `json_schema.schema` (JSON Schema object)

### Grammar dialect and caveats
- **Dialect:** appears to be **OpenAI-style `json_schema` structured output** (JSON Schema-based), not a published CFG/regex grammar DSL.
- **Caveats (documented):**
  - Structured output is listed as supported only for specific Phala models on that page.
  - No published spec for supported JSON Schema subset/limits (so treat unsupported keywords/features as unspecified).
  - Phala docs show a base URL inconsistency on Streaming page (`/api/v1`) vs other pages (`/v1`); structured-output examples use `/v1`.

### Streaming fields
For streamed output (SSE), documented chunks include:
- `choices[].delta.content`
- stream terminator: `data: [DONE]`
- No Phala-specific extra streaming fields for constrained output are documented (e.g., no grammar state/validator fields).

### Sources (URLs)
- https://docs.phala.com/phala-cloud/confidential-ai/confidential-model/structured-output
- https://docs.phala.com/phala-cloud/confidential-ai/confidential-model/streaming
- https://docs.phala.com/phala-cloud/confidential-ai/confidential-model/confidential-ai-api
- https://docs.redpill.ai/developers/api-reference/chat-completions
- https://docs.redpill.ai/developers/guides/streaming
tokens used
40,121
```

