## Provider
**Hyperbolic** (`https://api.hyperbolic.xyz/v1`) exposes chat via an OpenAI-compatible endpoint: `POST /chat/completions`.

## Grammar capability
- I found **no official Hyperbolic doc page** that documents CFG/grammar/regex constrained decoding fields.
- In Hyperbolic’s own parameter list for chat completions, there are no `grammar`, `regex`, `response_format`, `json_schema`, or `guided_*` fields documented.
- Hyperbolic does mention “instruct models are fine-tuned for ... structured outputs,” but this is a general claim, not a constrained-decoding API spec.

## Request shape
Documented request body fields on Hyperbolic chat completions include:
- `messages`, `model`
- sampling/control fields: `temperature`, `top_p`, `top_k`, `min_p`, `presence_penalty`, `frequency_penalty`, `repetition_penalty`, `stop`, `seed`
- output/logging fields: `max_tokens`, `n`, `logprobs`, `top_logprobs`, `logit_bias`
- streaming toggle: `stream`
- metadata: `user`

## Grammar dialect and caveats
- **Dialect:** Not documented by Hyperbolic (no BNF/EBNF/regex grammar spec found).
- **Caveat:** Because docs say “OpenAI-compatible,” unsupported-but-pass-through behavior is possible, but this is **inference**, not an official guarantee.
- For production, treat grammar-constrained decoding as **not officially specified** unless Hyperbolic publishes dedicated fields/docs.

## Streaming fields
From Hyperbolic’s streamed chunk examples (`stream: true`), relevant fields are:
- top-level: `id`, `model` (and sometimes `object: "chat.completion.chunk"`, `created`)
- `choices[]` entries with:
  - `index`
  - `delta.content` (token fragment)
  - `finish_reason` (`null` until final chunk, then e.g. `"stop"`)
- stream terminator: `data: [DONE]`

## Sources (URLs)
- https://docs.hyperbolic.xyz/docs/rest-api
- https://docs.hyperbolic.xyz/docs/inference-api
- https://docs.hyperbolic.xyz/docs/serverless-inference

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
session id: 019c5b0e-2f50-7813-ba50-182d396da368
--------
user
Research official documentation for provider "Hyperbolic" focused on grammar-constrained generation.
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
2026-02-14T07:29:42.248142Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5531-6c60-7612-b81c-b02333263b22
2026-02-14T07:29:42.268749Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5080-050b-7c53-92a8-9c52ce325359
2026-02-14T07:29:42.289389Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c58f2-9999-7e13-8897-cb3cb6765c62
2026-02-14T07:29:42.309995Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5ae2-4d18-7921-a6f9-9ca09a337133
2026-02-14T07:29:42.330703Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-1e63-7422-8df1-29cc3cd854ed
2026-02-14T07:29:42.351457Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-2af1-7321-8d40-367f5a3ba03a
2026-02-14T07:29:42.372097Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-8eca-7cf3-8c60-d66e26ea0144
2026-02-14T07:29:42.392658Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-1935-7772-bf75-7eb9d084599e
2026-02-14T07:29:42.413359Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-45eb-7810-9be4-e9c813827907
2026-02-14T07:29:42.434040Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-5630-7b30-8723-45187528edea
2026-02-14T07:29:42.454915Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0a-f457-71d1-902a-d41b0df6fafa
2026-02-14T07:29:42.475519Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0a-f500-7013-80bc-cc4e70470657
2026-02-14T07:29:42.496494Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-1200-74e2-b68a-b5695adf8ddc
2026-02-14T07:29:42.517246Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-4f6c-79a1-ad3e-23dd8a997ea2
2026-02-14T07:29:42.538216Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e2-75e1-99f8-269a75536055
2026-02-14T07:29:42.558836Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e0-7850-aab6-44bd39f1876c
2026-02-14T07:29:42.579625Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e3-7490-b15b-7731fbbd70ff
2026-02-14T07:29:42.600313Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-fd96-7c40-9fb5-4533f503a218
2026-02-14T07:29:42.620998Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-fd87-77a2-b52d-3b01e53fde37
2026-02-14T07:29:42.641755Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0d-db4c-7cc2-99b4-a433007462d2
2026-02-14T07:29:42.662512Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0d-f250-71f3-b5b4-0ea37af65fb7
2026-02-14T07:29:42.683322Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0d-f508-7283-bcc5-b2effda3a024
mcp: surrealdb ready
mcp: playwright ready
mcp: exa ready
mcp startup: ready: surrealdb, playwright, exa
🌐 Searching the web...
🌐 Searched: Hyperbolic official documentation grammar constrained generation CFG regex decoding

thinking
**Refining documentation search domain**
🌐 Searching the web...
🌐 Searched: Hyperbolic API docs structured outputs response_format grammar regex

thinking
**Exploring official hyperbolic docs**
🌐 Searching the web...
🌐 Searched: https://docs.hyperbolic.xyz/
🌐 Searching the web...
🌐 Searched: https://docs.hyperbolic.xyz/

thinking
**Planning click targets by ID**
🌐 Searching the web...
🌐 Searched: https://docs.hyperbolic.xyz/docs/inference-api

thinking
**Checking response format support**
🌐 Searching the web...
🌐 Searched: 'response_format' in https://docs.hyperbolic.xyz/docs/rest-api

thinking
**Exploring alternate API references**
🌐 Searching the web...
🌐 Searched: site:docs.hyperbolic.xyz "chat/completions" "response_format"

thinking
**Searching Hyperbolic OpenAPI docs**
🌐 Searching the web...
🌐 Searched: api.hyperbolic.xyz openapi

thinking
**Planning website reference endpoint**
🌐 Searching the web...
🌐 Searched the web

thinking
**Searching for updated reference path**
🌐 Searching the web...
🌐 Searched: site:docs.hyperbolic.xyz/reference "chat completion" "hyperbolic"

thinking
**Clarifying structured output support**
🌐 Searching the web...
🌐 Searched: https://docs.hyperbolic.xyz/docs/serverless-inference

thinking
**Summarizing provider docs with caveats**
codex
## Provider
**Hyperbolic** (`https://api.hyperbolic.xyz/v1`) exposes chat via an OpenAI-compatible endpoint: `POST /chat/completions`.

## Grammar capability
- I found **no official Hyperbolic doc page** that documents CFG/grammar/regex constrained decoding fields.
- In Hyperbolic’s own parameter list for chat completions, there are no `grammar`, `regex`, `response_format`, `json_schema`, or `guided_*` fields documented.
- Hyperbolic does mention “instruct models are fine-tuned for ... structured outputs,” but this is a general claim, not a constrained-decoding API spec.

## Request shape
Documented request body fields on Hyperbolic chat completions include:
- `messages`, `model`
- sampling/control fields: `temperature`, `top_p`, `top_k`, `min_p`, `presence_penalty`, `frequency_penalty`, `repetition_penalty`, `stop`, `seed`
- output/logging fields: `max_tokens`, `n`, `logprobs`, `top_logprobs`, `logit_bias`
- streaming toggle: `stream`
- metadata: `user`

## Grammar dialect and caveats
- **Dialect:** Not documented by Hyperbolic (no BNF/EBNF/regex grammar spec found).
- **Caveat:** Because docs say “OpenAI-compatible,” unsupported-but-pass-through behavior is possible, but this is **inference**, not an official guarantee.
- For production, treat grammar-constrained decoding as **not officially specified** unless Hyperbolic publishes dedicated fields/docs.

## Streaming fields
From Hyperbolic’s streamed chunk examples (`stream: true`), relevant fields are:
- top-level: `id`, `model` (and sometimes `object: "chat.completion.chunk"`, `created`)
- `choices[]` entries with:
  - `index`
  - `delta.content` (token fragment)
  - `finish_reason` (`null` until final chunk, then e.g. `"stop"`)
- stream terminator: `data: [DONE]`

## Sources (URLs)
- https://docs.hyperbolic.xyz/docs/rest-api
- https://docs.hyperbolic.xyz/docs/inference-api
- https://docs.hyperbolic.xyz/docs/serverless-inference
tokens used
33,714
```

