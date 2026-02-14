### Provider
**GMI Cloud (Inference Engine, OpenAI-compatible endpoints)**

### Grammar capability
- **Documented support:** JSON mode via `response_format`.
- **Not documented:** grammar-constrained decoding via CFG, regex, or custom grammar definitions.
- As of **2026-02-14**, official docs only explicitly show `response_format: {"type":"json_object"}`.

### Request shape
`POST https://api.gmi-serving.com/v1/chat/completions`

Relevant fields for constrained output:
- `response_format` (object): “Force output format (e.g., JSON)”
- `stream` (boolean): stream partial progress

Documented example:
```json
{
  "response_format": { "type": "json_object" },
  "stream": true
}
```

### Grammar dialect and caveats
- **Dialect:** No grammar dialect is specified (no CFG/BNF/PEG/regex schema documented).
- **Caveat:** Capability appears limited (in docs) to JSON-object mode, not full grammar-constrained decoding.
- Docs also note parameter support can vary by model.

### Streaming fields
- `stream: true` enables streaming.
- Docs explicitly state: **usage stats are included in the final streaming chunk**.
- No detailed documented streaming chunk schema specific to constrained/grammar output was found.

### Sources (URLs)
- https://docs.gmicloud.ai/inference-engine/api-reference/llm-api-reference
- https://docs.gmicloud.ai/inference-engine/ie-intro

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
session id: 019c5b0d-f250-71f3-b5b4-0ea37af65fb7
--------
user
Research official documentation for provider "GMICloud" focused on grammar-constrained generation.
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
mcp: playwright starting
mcp: exa starting
2026-02-14T07:29:26.632192Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5531-6c60-7612-b81c-b02333263b22
2026-02-14T07:29:26.652818Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5080-050b-7c53-92a8-9c52ce325359
2026-02-14T07:29:26.673577Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c58f2-9999-7e13-8897-cb3cb6765c62
2026-02-14T07:29:26.694332Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5ae2-4d18-7921-a6f9-9ca09a337133
2026-02-14T07:29:26.714919Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-1e63-7422-8df1-29cc3cd854ed
2026-02-14T07:29:26.735685Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-2af1-7321-8d40-367f5a3ba03a
2026-02-14T07:29:26.756503Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-8eca-7cf3-8c60-d66e26ea0144
2026-02-14T07:29:26.777299Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-1935-7772-bf75-7eb9d084599e
2026-02-14T07:29:26.797959Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-45eb-7810-9be4-e9c813827907
2026-02-14T07:29:26.818663Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-5630-7b30-8723-45187528edea
2026-02-14T07:29:26.839241Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0a-f457-71d1-902a-d41b0df6fafa
2026-02-14T07:29:26.859973Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0a-f500-7013-80bc-cc4e70470657
2026-02-14T07:29:26.880724Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-1200-74e2-b68a-b5695adf8ddc
2026-02-14T07:29:26.901345Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-4f6c-79a1-ad3e-23dd8a997ea2
2026-02-14T07:29:26.922057Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e2-75e1-99f8-269a75536055
2026-02-14T07:29:26.942766Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e0-7850-aab6-44bd39f1876c
2026-02-14T07:29:26.963571Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e3-7490-b15b-7731fbbd70ff
2026-02-14T07:29:26.984346Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-fd96-7c40-9fb5-4533f503a218
2026-02-14T07:29:27.005490Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-fd87-77a2-b52d-3b01e53fde37
2026-02-14T07:29:27.026157Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-fd87-7a13-a28a-bd0bb5eb39b5
2026-02-14T07:29:27.047010Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-fd86-7282-9d41-25a8785365db
2026-02-14T07:29:27.067867Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0d-db4c-7cc2-99b4-a433007462d2
mcp: surrealdb ready
mcp: playwright ready
mcp: exa ready
mcp startup: ready: surrealdb, playwright, exa

thinking
**Planning targeted web research**
🌐 Searching the web...
🌐 Searched: GMICloud official documentation grammar constrained decoding regex CFG streaming fields

thinking
**Investigating official API endpoints**
🌐 Searching the web...
🌐 Searched: site:docs.gmicloud.ai GMICloud OpenAI compatible API response_format json_schema stream
🌐 Searching the web...
🌐 Searched: https://docs.gmicloud.ai/inference-engine/api-reference/llm-api-reference

thinking
**Searching for responses API schema**
🌐 Searching the web...
🌐 Searched: site:docs.gmicloud.ai "Responses" "response_format" "json_schema"

thinking
**Exploring inference overview page**
🌐 Searching the web...
🌐 Searched the web

thinking
**Planning use of ref links**
🌐 Searching the web...
🌐 Searched: https://docs.gmicloud.ai/inference-engine/ie-intro

thinking
**Verifying JSON streaming schema**
🌐 Searching the web...
🌐 Searched: site:docs.gmicloud.ai "json_schema"

thinking
**Considering API-reference structure**
🌐 Searching the web...
🌐 Searched: https://docs.gmicloud.ai/inference-engine/api-reference

thinking
**Searching for response format docs**
🌐 Searching the web...
🌐 Searched: site:docs.gmicloud.ai "Responses API" "GMI"

thinking
**Checking grammar and regex support**
🌐 Searching the web...
🌐 Searched: site:docs.gmicloud.ai regex constrained decoding

thinking
**Confirming model parameter documentation**
codex
### Provider
**GMI Cloud (Inference Engine, OpenAI-compatible endpoints)**

### Grammar capability
- **Documented support:** JSON mode via `response_format`.
- **Not documented:** grammar-constrained decoding via CFG, regex, or custom grammar definitions.
- As of **2026-02-14**, official docs only explicitly show `response_format: {"type":"json_object"}`.

### Request shape
`POST https://api.gmi-serving.com/v1/chat/completions`

Relevant fields for constrained output:
- `response_format` (object): “Force output format (e.g., JSON)”
- `stream` (boolean): stream partial progress

Documented example:
```json
{
  "response_format": { "type": "json_object" },
  "stream": true
}
```

### Grammar dialect and caveats
- **Dialect:** No grammar dialect is specified (no CFG/BNF/PEG/regex schema documented).
- **Caveat:** Capability appears limited (in docs) to JSON-object mode, not full grammar-constrained decoding.
- Docs also note parameter support can vary by model.

### Streaming fields
- `stream: true` enables streaming.
- Docs explicitly state: **usage stats are included in the final streaming chunk**.
- No detailed documented streaming chunk schema specific to constrained/grammar output was found.

### Sources (URLs)
- https://docs.gmicloud.ai/inference-engine/api-reference/llm-api-reference
- https://docs.gmicloud.ai/inference-engine/ie-intro
tokens used
22,129
```

