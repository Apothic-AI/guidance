## Provider
**NextBit (via OpenRouter provider routing)**  
Official provider page is on OpenRouter (`provider` slug: `nextbit`).

## Grammar capability
- **No official NextBit-specific docs found for CFG/BNF/regex constrained decoding fields.**
- On OpenRouter, constrained output is documented as:
  - `response_format: { "type": "json_object" }` (JSON mode)
  - `response_format: { "type": "json_schema", "json_schema": {...} }` (schema-constrained output)
- Inference: for NextBit on OpenRouter, grammar-style control appears to be **JSON-schema structured output**, not explicit CFG/regex APIs.

## Request shape
- Core constrained-output request fields:
  - `response_format` (map)
  - `response_format.type`: `json_object` or `json_schema`
  - `response_format.json_schema`: `{ name, strict, schema }` (for `json_schema`)
- Routing to NextBit specifically:
  - `provider: { "order": ["nextbit"] }` or `provider: { "only": ["nextbit"] }`
- Compatibility guard:
  - `provider.require_parameters: true` to ensure routed provider supports all requested params.

## Grammar dialect and caveats
- Dialect documented: **JSON Schema** (for `response_format.type = "json_schema"`).
- No documented NextBit-native CFG/EBNF/regex grammar dialect in official NextBit/OpenRouter provider docs.
- Caveats:
  - `supported_parameters` in model listings are a **union across providers**; one provider may not support all listed params.
  - Use `provider.require_parameters: true` when you need strict parameter support.
  - `strict: true` is recommended in `json_schema`.

## Streaming fields
- Enable with `stream: true`.
- Relevant chunk fields for constrained output streams:
  - `choices[0].delta.content` (partial text/JSON)
  - `choices[0].finish_reason`
  - `usage` (final chunk includes usage stats)
- Mid-stream error event can include:
  - top-level `error`
  - `provider`
  - `choices[0].finish_reason: "error"`

## Sources (URLs)
- https://openrouter.ai/provider/nextbit  
- https://openrouter.ai/docs/guides/features/structured-outputs  
- https://openrouter.ai/docs/api/reference/parameters  
- https://openrouter.ai/docs/guides/routing/provider-selection  
- https://openrouter.ai/docs/api/reference/streaming  
- https://openrouter.ai/docs/api-reference/list-available-models

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
session id: 019c5b0e-4ff4-7c11-809c-677b76971da0
--------
user
Research official documentation for provider "NextBit" focused on grammar-constrained generation.
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
mcp: playwright starting
mcp: surrealdb starting
2026-02-14T07:29:50.612578Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5531-6c60-7612-b81c-b02333263b22
2026-02-14T07:29:50.626923Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5080-050b-7c53-92a8-9c52ce325359
2026-02-14T07:29:50.648232Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c58f2-9999-7e13-8897-cb3cb6765c62
2026-02-14T07:29:50.669084Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5ae2-4d18-7921-a6f9-9ca09a337133
2026-02-14T07:29:50.689725Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-1e63-7422-8df1-29cc3cd854ed
2026-02-14T07:29:50.710496Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-2af1-7321-8d40-367f5a3ba03a
2026-02-14T07:29:50.731243Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-8eca-7cf3-8c60-d66e26ea0144
2026-02-14T07:29:50.752006Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-1935-7772-bf75-7eb9d084599e
2026-02-14T07:29:50.772795Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-45eb-7810-9be4-e9c813827907
2026-02-14T07:29:50.793614Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-5630-7b30-8723-45187528edea
2026-02-14T07:29:50.814355Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0a-f457-71d1-902a-d41b0df6fafa
2026-02-14T07:29:50.835188Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0a-f500-7013-80bc-cc4e70470657
2026-02-14T07:29:50.855891Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-1200-74e2-b68a-b5695adf8ddc
2026-02-14T07:29:50.876738Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-4f6c-79a1-ad3e-23dd8a997ea2
2026-02-14T07:29:50.897492Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e2-75e1-99f8-269a75536055
2026-02-14T07:29:50.918487Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e0-7850-aab6-44bd39f1876c
2026-02-14T07:29:50.939342Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e3-7490-b15b-7731fbbd70ff
2026-02-14T07:29:50.960052Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0d-db4c-7cc2-99b4-a433007462d2
2026-02-14T07:29:50.980824Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0d-f250-71f3-b5b4-0ea37af65fb7
2026-02-14T07:29:51.001657Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0d-f508-7283-bcc5-b2effda3a024
2026-02-14T07:29:51.022939Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0e-2f50-7813-ba50-182d396da368
2026-02-14T07:29:51.043630Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0e-4762-75c1-b6a7-713ce89707a2
mcp: surrealdb ready
mcp: playwright ready
mcp: exa ready
mcp startup: ready: surrealdb, playwright, exa

thinking
**Planning official docs search**
codex
I’ll identify NextBit’s official API docs first, then verify constrained-decoding support and extract exact request/streaming fields from primary documentation pages.
🌐 Searching the web...
🌐 Searched: NextBit API documentation grammar constrained decoding CFG regex

thinking
**Researching NextBit provider origin**
codex
Search results were noisy, so I’m narrowing to authoritative pages for “NextBit” itself and provider docs that describe constrained decoding fields.
🌐 Searching the web...
🌐 Searched: "NextBit" AI provider docs

thinking
**Investigating NextBit provider docs**
codex
I found that “NextBit” appears as an OpenRouter provider; now I’m checking OpenRouter’s official docs for provider-routing and constrained output fields, plus whether NextBit exposes any provider-specific grammar controls.
🌐 Searching the web...
🌐 Searched: site:openrouter.ai/docs nextbit provider

thinking
**Exploring streaming detail options**
codex
I’ve confirmed constrained output is documented at OpenRouter level; next I’m pulling the streaming schema and parameter compatibility details needed to answer precisely for NextBit routing.
🌐 Searching the web...
🌐 Searched: site:openrouter.ai/docs streaming chat completions SSE choices delta

thinking
**Considering provider-specific nextbit integration**
🌐 Searching the web...
🌐 Searched: site:openrouter.ai nextbit provider slug nextbit

thinking
**Inspecting provider constraint page**
🌐 Searching the web...
🌐 Searched: https://openrouter.ai/provider/nextbit

thinking
**Planning OpenAPI field extraction**
codex
I found the official NextBit provider page on OpenRouter, but it does not document provider-specific grammar features. I’m now extracting exact API field names from OpenRouter’s reference/OpenAPI so the request and streaming sections are precise.
🌐 Searching the web...
🌐 Searched: https://openrouter.ai/openapi.json

thinking
**Identifying limitation in OpenAPI exploration**
🌐 Searching the web...
🌐 Searched: 'response_format' in https://openrouter.ai/openapi.json

thinking
**Assessing streaming fields and parameters**
codex
I have enough to answer with high confidence: NextBit’s official surface is via OpenRouter provider routing, and constrained output support appears to be JSON Schema (`response_format`) rather than CFG/regex fields. I’m validating final field names for streaming chunks and usage event now.
🌐 Searching the web...
🌐 Searched: https://openrouter.ai/docs/api/reference/streaming

thinking
**Searching response format marker**
🌐 Searching the web...
🌐 Searched: 'response_format' in https://openrouter.ai/docs/features/structured-outputs

thinking
**Locating provider routing requirements**
🌐 Searching the web...
🌐 Searched: https://openrouter.ai/docs/features/provider-routing

thinking
**Clarifying parameter support and caveats**
codex
## Provider
**NextBit (via OpenRouter provider routing)**  
Official provider page is on OpenRouter (`provider` slug: `nextbit`).

## Grammar capability
- **No official NextBit-specific docs found for CFG/BNF/regex constrained decoding fields.**
- On OpenRouter, constrained output is documented as:
  - `response_format: { "type": "json_object" }` (JSON mode)
  - `response_format: { "type": "json_schema", "json_schema": {...} }` (schema-constrained output)
- Inference: for NextBit on OpenRouter, grammar-style control appears to be **JSON-schema structured output**, not explicit CFG/regex APIs.

## Request shape
- Core constrained-output request fields:
  - `response_format` (map)
  - `response_format.type`: `json_object` or `json_schema`
  - `response_format.json_schema`: `{ name, strict, schema }` (for `json_schema`)
- Routing to NextBit specifically:
  - `provider: { "order": ["nextbit"] }` or `provider: { "only": ["nextbit"] }`
- Compatibility guard:
  - `provider.require_parameters: true` to ensure routed provider supports all requested params.

## Grammar dialect and caveats
- Dialect documented: **JSON Schema** (for `response_format.type = "json_schema"`).
- No documented NextBit-native CFG/EBNF/regex grammar dialect in official NextBit/OpenRouter provider docs.
- Caveats:
  - `supported_parameters` in model listings are a **union across providers**; one provider may not support all listed params.
  - Use `provider.require_parameters: true` when you need strict parameter support.
  - `strict: true` is recommended in `json_schema`.

## Streaming fields
- Enable with `stream: true`.
- Relevant chunk fields for constrained output streams:
  - `choices[0].delta.content` (partial text/JSON)
  - `choices[0].finish_reason`
  - `usage` (final chunk includes usage stats)
- Mid-stream error event can include:
  - top-level `error`
  - `provider`
  - `choices[0].finish_reason: "error"`

## Sources (URLs)
- https://openrouter.ai/provider/nextbit  
- https://openrouter.ai/docs/guides/features/structured-outputs  
- https://openrouter.ai/docs/api/reference/parameters  
- https://openrouter.ai/docs/guides/routing/provider-selection  
- https://openrouter.ai/docs/api/reference/streaming  
- https://openrouter.ai/docs/api-reference/list-available-models
tokens used
56,043
```

