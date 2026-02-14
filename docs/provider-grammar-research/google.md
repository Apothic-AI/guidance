## Provider
Google (Gemini API / Generative Language API)

## Grammar capability
- No explicit CFG/BNF/regex-constrained decoding interface is documented.
- Officially supported constrained output is **schema-constrained JSON** (and enum text mode), via structured outputs.

## Request shape
- Endpoint patterns:
  - `models/*:generateContent`
  - `models/*:streamGenerateContent`
- Constrained-output fields live in generation config:
  - `responseMimeType` (notably `application/json`, `text/x.enum`)
  - `responseSchema` (OpenAPI-subset schema object)
  - `responseJsonSchema` (JSON Schema value; use instead of `responseSchema`)
- Constraint noted by docs:
  - If `responseJsonSchema` is set, `responseSchema` must be omitted, and `responseMimeType` is required (`application/json` for JSON schema output).

## Grammar dialect and caveats
- Dialect support is **JSON Schema subset** (plus an OpenAPI-based schema option).
- Supported JSON Schema properties include: `$id`, `$defs`, `$ref`, `$anchor`, `type`, `format`, `title`, `description`, `enum`, `items`, `prefixItems`, `minItems`, `maxItems`, `minimum`, `maximum`, `anyOf`, `oneOf` (treated like `anyOf`), `properties`, `additionalProperties`, `required`.
- Non-standard `propertyOrdering` is supported.
- Caveats:
  - Not full JSON Schema support.
  - Cyclic refs are limited/unrolled and restricted.
  - Very complex schemas may be rejected.
  - Docs guarantee syntactically valid JSON for structured outputs, not semantic correctness.

## Streaming fields
- Streaming method returns a stream of `GenerateContentResponse` objects.
- Relevant chunk access pattern in official examples:
  - `chunk.candidates[0].content.parts[0].text`
- Structured-output streaming note:
  - Chunks are valid **partial JSON strings** that can be concatenated into the final JSON object.
- Response-level fields include `candidates[]`, `promptFeedback`, `usageMetadata`, `modelVersion`, `responseId`, `modelStatus`.

## Sources (URLs)
- https://ai.google.dev/gemini-api/docs/structured-output
- https://ai.google.dev/api/generate-content#v1beta.CitationMetadata

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
session id: 019c5b0d-f508-7283-bcc5-b2effda3a024
--------
user
Research official documentation for provider "Google" focused on grammar-constrained generation.
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
2026-02-14T07:29:27.334575Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5531-6c60-7612-b81c-b02333263b22
2026-02-14T07:29:27.355542Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5080-050b-7c53-92a8-9c52ce325359
2026-02-14T07:29:27.376328Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c58f2-9999-7e13-8897-cb3cb6765c62
2026-02-14T07:29:27.397088Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5ae2-4d18-7921-a6f9-9ca09a337133
2026-02-14T07:29:27.417868Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-1e63-7422-8df1-29cc3cd854ed
2026-02-14T07:29:27.438579Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-2af1-7321-8d40-367f5a3ba03a
2026-02-14T07:29:27.459727Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-8eca-7cf3-8c60-d66e26ea0144
2026-02-14T07:29:27.480505Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-1935-7772-bf75-7eb9d084599e
2026-02-14T07:29:27.502245Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-45eb-7810-9be4-e9c813827907
2026-02-14T07:29:27.523734Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-5630-7b30-8723-45187528edea
2026-02-14T07:29:27.544982Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0a-f457-71d1-902a-d41b0df6fafa
2026-02-14T07:29:27.565672Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0a-f500-7013-80bc-cc4e70470657
2026-02-14T07:29:27.586627Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-1200-74e2-b68a-b5695adf8ddc
2026-02-14T07:29:27.607353Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-4f6c-79a1-ad3e-23dd8a997ea2
2026-02-14T07:29:27.629487Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e2-75e1-99f8-269a75536055
2026-02-14T07:29:27.650371Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e0-7850-aab6-44bd39f1876c
2026-02-14T07:29:27.671111Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e3-7490-b15b-7731fbbd70ff
2026-02-14T07:29:27.691903Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-fd96-7c40-9fb5-4533f503a218
2026-02-14T07:29:27.712844Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-fd87-77a2-b52d-3b01e53fde37
2026-02-14T07:29:27.733685Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-fd87-7a13-a28a-bd0bb5eb39b5
2026-02-14T07:29:27.754723Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0d-db4c-7cc2-99b4-a433007462d2
2026-02-14T07:29:27.778028Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0d-f250-71f3-b5b4-0ea37af65fb7
mcp: surrealdb ready
mcp: playwright ready
mcp: exa ready
mcp startup: ready: surrealdb, playwright, exa

thinking
**Scoping official docs search**
🌐 Searching the web...
🌐 Searched: Google Gemini API grammar constrained decoding CFG regex documentation

thinking
**Verifying official API schemas**
🌐 Searching the web...
🌐 Searched: ai.google.dev Gemini API structured output responseMimeType responseSchema responseJsonSchema

thinking
**Reviewing documentation references**
🌐 Searching the web...
🌐 Searched: https://ai.google.dev/gemini-api/docs/structured-output

thinking
**Searching for config patterns**
🌐 Searching the web...
🌐 Searched: 'responseMimeType' in https://ai.google.dev/api/rest/generativelanguage/CitationMetadata

thinking
**Planning deeper response parsing**
🌐 Searching the web...
🌐 Searched: https://ai.google.dev/api/rest/generativelanguage/CitationMetadata

thinking
**Identifying JSON schema support range**
🌐 Searching the web...
🌐 Searched: https://ai.google.dev/api/rest/generativelanguage/CitationMetadata

thinking
**Identifying streaming JSON patterns**
🌐 Searching the web...
🌐 Searched: 'valid partial JSON strings' in https://ai.google.dev/gemini-api/docs/structured-output

thinking
**Checking for regex or CFG references**
🌐 Searching the web...
🌐 Searched: 'regex' in https://ai.google.dev/gemini-api/docs/structured-output

thinking
**Preparing intermediary commentary**
codex
I checked Google’s official Gemini API docs and extracted the exact constrained-output fields (`responseMimeType`, `responseSchema`, `responseJsonSchema`) plus streaming response structure. I’m now compiling a concise provider summary, including whether CFG/regex grammar decoding is explicitly supported.
codex
## Provider
Google (Gemini API / Generative Language API)

## Grammar capability
- No explicit CFG/BNF/regex-constrained decoding interface is documented.
- Officially supported constrained output is **schema-constrained JSON** (and enum text mode), via structured outputs.

## Request shape
- Endpoint patterns:
  - `models/*:generateContent`
  - `models/*:streamGenerateContent`
- Constrained-output fields live in generation config:
  - `responseMimeType` (notably `application/json`, `text/x.enum`)
  - `responseSchema` (OpenAPI-subset schema object)
  - `responseJsonSchema` (JSON Schema value; use instead of `responseSchema`)
- Constraint noted by docs:
  - If `responseJsonSchema` is set, `responseSchema` must be omitted, and `responseMimeType` is required (`application/json` for JSON schema output).

## Grammar dialect and caveats
- Dialect support is **JSON Schema subset** (plus an OpenAPI-based schema option).
- Supported JSON Schema properties include: `$id`, `$defs`, `$ref`, `$anchor`, `type`, `format`, `title`, `description`, `enum`, `items`, `prefixItems`, `minItems`, `maxItems`, `minimum`, `maximum`, `anyOf`, `oneOf` (treated like `anyOf`), `properties`, `additionalProperties`, `required`.
- Non-standard `propertyOrdering` is supported.
- Caveats:
  - Not full JSON Schema support.
  - Cyclic refs are limited/unrolled and restricted.
  - Very complex schemas may be rejected.
  - Docs guarantee syntactically valid JSON for structured outputs, not semantic correctness.

## Streaming fields
- Streaming method returns a stream of `GenerateContentResponse` objects.
- Relevant chunk access pattern in official examples:
  - `chunk.candidates[0].content.parts[0].text`
- Structured-output streaming note:
  - Chunks are valid **partial JSON strings** that can be concatenated into the final JSON object.
- Response-level fields include `candidates[]`, `promptFeedback`, `usageMetadata`, `modelVersion`, `responseId`, `modelStatus`.

## Sources (URLs)
- https://ai.google.dev/gemini-api/docs/structured-output
- https://ai.google.dev/api/generate-content#v1beta.CitationMetadata
tokens used
31,002
```

