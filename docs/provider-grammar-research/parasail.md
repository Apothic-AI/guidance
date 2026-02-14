## Provider
**Parasail** (OpenAI-compatible API), with chat endpoint documented at `https://api.parasail.io/v1` (one cookbook snippet also shows `https://api.parasail.ai/v1`).

## Grammar capability
- **Regex constrained decoding:** **Yes** (documented).
- **JSON-schema constrained decoding:** **Yes** (documented).
- **CFG / grammar-string constrained decoding:** **Not explicitly documented by Parasail**.
- **Inference:** Parasail says it supports vLLM parameters; vLLM supports `guided_grammar` (CFG), but Parasail docs do not explicitly promise this field works on their hosted API.

## Request shape
- Endpoint pattern: `POST /v1/chat/completions` (OpenAI-compatible).
- Documented constrained-output fields on Parasail:
  - `structured_output: <json-schema-object>`  
  - `structured_output: "dict"`  
  - `structured_output: "<regex-pattern>"`
- Also documented in Parasail Python example (OpenAI client):
  - `extra_body: { "guided_json": { ...schema... } }`
- Streaming note in Parasail docs: use `stream=true`; constraints still apply.

## Grammar dialect and caveats
- **Regex dialect:** not specified in Parasail docs.
- **JSON Schema dialect/subset:** Parasail says formats are based on OpenAI specs; no Parasail-specific schema-dialect profile published.
- **Model support is model-dependent** (Parasail provides a support matrix in the structured-output cookbook).
- Parasail troubleshooting caveat: if constraints are weakly followed, put schema/regex in both prompt and structured field.
- Minor doc inconsistency: both `api.parasail.io` and `api.parasail.ai` appear in examples.

## Streaming fields
- Parasail docs confirm constrained output can be streamed (`stream=true`) but do **not** publish a Parasail-specific streaming chunk schema.
- **Inference from Parasail’s OpenAI-compatibility claim:** expect standard Chat Completions SSE chunk fields such as `choices[].delta.content` and terminal `choices[].finish_reason` / `[DONE]`.

## Sources (URLs)
- https://docs.parasail.io/parasail-docs/cookbooks/structured-output  
- https://docs.parasail.io/parasail-docs/serverless-and-models/available-parameters  
- https://docs.parasail.io/parasail-docs/serverless-and-models/serverless  
- https://docs.parasail.io/parasail-docs/batch/api-reference  
- https://docs.vllm.ai/en/v0.6.6.post1/usage/structured_outputs.html  
- https://docs.vllm.ai/en/v0.9.0/api/vllm/model_executor/guided_decoding/guided_fields.html  
- https://platform.openai.com/docs/api-reference/chat/create-chat-completion

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
session id: 019c5b0e-b4b5-7fe2-a3e5-58d9a3aefdc9
--------
user
Research official documentation for provider "Parasail" focused on grammar-constrained generation.
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
2026-02-14T07:30:16.397840Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5531-6c60-7612-b81c-b02333263b22
2026-02-14T07:30:16.418602Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5080-050b-7c53-92a8-9c52ce325359
2026-02-14T07:30:16.439462Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c58f2-9999-7e13-8897-cb3cb6765c62
2026-02-14T07:30:16.460145Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5ae2-4d18-7921-a6f9-9ca09a337133
2026-02-14T07:30:16.480755Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-1e63-7422-8df1-29cc3cd854ed
2026-02-14T07:30:16.501353Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-2af1-7321-8d40-367f5a3ba03a
2026-02-14T07:30:16.522242Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-8eca-7cf3-8c60-d66e26ea0144
2026-02-14T07:30:16.542915Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-1935-7772-bf75-7eb9d084599e
2026-02-14T07:30:16.563684Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-45eb-7810-9be4-e9c813827907
2026-02-14T07:30:16.584622Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-5630-7b30-8723-45187528edea
2026-02-14T07:30:16.605424Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0a-f457-71d1-902a-d41b0df6fafa
2026-02-14T07:30:16.626081Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0a-f500-7013-80bc-cc4e70470657
2026-02-14T07:30:16.646998Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-1200-74e2-b68a-b5695adf8ddc
2026-02-14T07:30:16.667627Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-4f6c-79a1-ad3e-23dd8a997ea2
2026-02-14T07:30:16.688241Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e2-75e1-99f8-269a75536055
2026-02-14T07:30:16.708894Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e0-7850-aab6-44bd39f1876c
2026-02-14T07:30:16.720742Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e3-7490-b15b-7731fbbd70ff
2026-02-14T07:30:16.741571Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0d-f508-7283-bcc5-b2effda3a024
2026-02-14T07:30:16.762182Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0e-2f50-7813-ba50-182d396da368
2026-02-14T07:30:16.782963Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0e-4762-75c1-b6a7-713ce89707a2
2026-02-14T07:30:16.804250Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0e-4ff4-7c11-809c-677b76971da0
2026-02-14T07:30:16.825016Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0e-7fe1-7683-ad3b-c244133d6497
mcp: surrealdb ready
mcp: playwright ready
mcp: exa ready
mcp startup: ready: surrealdb, playwright, exa

thinking
**Planning web search for docs**
🌐 Searching the web...
🌐 Searched: Parasail API documentation grammar constrained generation CFG regex decoding

thinking
**Exploring docs for JSON and streaming details**
🌐 Searching the web...
🌐 Searched: https://docs.parasail.io/parasail-docs/cookbooks/structured-output

thinking
**Gathering detailed API parameter info**
🌐 Searching the web...
🌐 Searched: https://docs.parasail.io/parasail-docs/serverless-and-models/available-parameters

thinking
**Exploring serverless decoding fields**
🌐 Searching the web...
🌐 Searched: https://docs.parasail.io/parasail-docs/serverless-and-models/serverless

thinking
**Identifying streaming fields source**
🌐 Searching the web...
🌐 Searched: https://docs.parasail.io/parasail-docs/cookbooks/chat-completions

thinking
**Searching for OpenAPI spec**
🌐 Searching the web...
🌐 Searched: site:docs.parasail.io openapi.json parasail chat completions stream delta

thinking
**Analyzing Parasail and OpenAI constrained decoding docs**
🌐 Searching the web...
🌐 Searched: https://docs.parasail.io/parasail-docs/batch/api-reference

thinking
**Referencing OpenAI streaming fields**
🌐 Searching the web...
🌐 Searched: OpenAI chat completions streaming chunk fields delta finish_reason
🌐 Searching the web...
🌐 Searched: OpenAI chat completions streaming chunk fields delta finish_reason

thinking
**Identifying API domain inconsistency**
🌐 Searching the web...
🌐 Searched: https://platform.openai.com/docs/api-reference/chat/create-chat-completion

thinking
**Exploring API spec for fields**
🌐 Searching the web...
🌐 Searched the web

thinking
**Noting need for exact URL search**
🌐 Searching the web...
🌐 Searched: api.parasail.io openapi.json

thinking
**Clarifying streaming response fields**
🌐 Searching the web...
🌐 Searched: site:platform.openai.com ChatCompletionChunk object choices delta role content finish_reason

thinking
**Summarizing Parasail OpenAI compatibility**
codex
## Provider
**Parasail** (OpenAI-compatible API), with chat endpoint documented at `https://api.parasail.io/v1` (one cookbook snippet also shows `https://api.parasail.ai/v1`).

## Grammar capability
- **Regex constrained decoding:** **Yes** (documented).
- **JSON-schema constrained decoding:** **Yes** (documented).
- **CFG / grammar-string constrained decoding:** **Not explicitly documented by Parasail**.
- **Inference:** Parasail says it supports vLLM parameters; vLLM supports `guided_grammar` (CFG), but Parasail docs do not explicitly promise this field works on their hosted API.

## Request shape
- Endpoint pattern: `POST /v1/chat/completions` (OpenAI-compatible).
- Documented constrained-output fields on Parasail:
  - `structured_output: <json-schema-object>`  
  - `structured_output: "dict"`  
  - `structured_output: "<regex-pattern>"`
- Also documented in Parasail Python example (OpenAI client):
  - `extra_body: { "guided_json": { ...schema... } }`
- Streaming note in Parasail docs: use `stream=true`; constraints still apply.

## Grammar dialect and caveats
- **Regex dialect:** not specified in Parasail docs.
- **JSON Schema dialect/subset:** Parasail says formats are based on OpenAI specs; no Parasail-specific schema-dialect profile published.
- **Model support is model-dependent** (Parasail provides a support matrix in the structured-output cookbook).
- Parasail troubleshooting caveat: if constraints are weakly followed, put schema/regex in both prompt and structured field.
- Minor doc inconsistency: both `api.parasail.io` and `api.parasail.ai` appear in examples.

## Streaming fields
- Parasail docs confirm constrained output can be streamed (`stream=true`) but do **not** publish a Parasail-specific streaming chunk schema.
- **Inference from Parasail’s OpenAI-compatibility claim:** expect standard Chat Completions SSE chunk fields such as `choices[].delta.content` and terminal `choices[].finish_reason` / `[DONE]`.

## Sources (URLs)
- https://docs.parasail.io/parasail-docs/cookbooks/structured-output  
- https://docs.parasail.io/parasail-docs/serverless-and-models/available-parameters  
- https://docs.parasail.io/parasail-docs/serverless-and-models/serverless  
- https://docs.parasail.io/parasail-docs/batch/api-reference  
- https://docs.vllm.ai/en/v0.6.6.post1/usage/structured_outputs.html  
- https://docs.vllm.ai/en/v0.9.0/api/vllm/model_executor/guided_decoding/guided_fields.html  
- https://platform.openai.com/docs/api-reference/chat/create-chat-completion
tokens used
49,646
```

