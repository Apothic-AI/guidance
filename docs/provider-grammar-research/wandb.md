## Provider
**W&B Inference** (`https://api.inference.wandb.ai/v1`), documented as an **OpenAI-compatible** Chat Completions API.

## Grammar capability
- **Documented support:** schema-constrained output via `response_format.type = "json_schema"`.
- **Not documented in W&B Inference docs:** direct CFG grammar strings or regex-constrained decoding request params (e.g., no documented `guided_grammar`/`guided_regex` in Inference pages).

## Request shape
Use Chat Completions with:
```json
{
  "model": "...",
  "messages": [...],
  "response_format": {
    "type": "json_schema",
    "json_schema": {
      "name": "YourSchemaName",
      "strict": true,
      "schema": { "...": "JSON Schema object" }
    }
  },
  "stream": true
}
```
Key constrained-output fields are:
- `response_format.type`
- `response_format.json_schema.name`
- `response_format.json_schema.strict`
- `response_format.json_schema.schema`

## Grammar dialect and caveats
- Dialect is effectively **JSON Schema-based structured output** (not an exposed CFG/regex DSL in Inference docs).
- W&B positions this as preferred over JSON mode for schema adherence.
- Because it is OpenAI-compatible, behavior is framed as OpenAI-format structured output rather than a custom grammar engine.

## Streaming fields
For streaming (`stream: true`), W&B examples show:
- token chunks via `chunk.choices[0].delta.content`
- plus usage-style chunk(s) where `chunk.choices` may be empty (example comment: “Show CompletionUsage object”)

Relevant completion fields (non-stream example) remain OpenAI-style:
- `choices[].message.content`
- `choices[].finish_reason`
- `usage.*`

## Sources (URLs)
- https://docs.wandb.ai/inference  
- https://docs.wandb.ai/inference/api-reference  
- https://docs.wandb.ai/inference/api-reference/chat-completions  
- https://docs.wandb.ai/inference/response-settings/structured-output  
- https://docs.wandb.ai/inference/response-settings/streaming  
- (Contrast, different product/API): https://docs.wandb.ai/training/api-reference/chat-completions/create-chat-completion-1

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
session id: 019c5b0f-32f7-7891-bca9-59d526279265
--------
user
Research official documentation for provider "WandB" focused on grammar-constrained generation.
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
2026-02-14T07:30:48.721670Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5531-6c60-7612-b81c-b02333263b22
2026-02-14T07:30:48.742737Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5080-050b-7c53-92a8-9c52ce325359
2026-02-14T07:30:48.763453Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c58f2-9999-7e13-8897-cb3cb6765c62
2026-02-14T07:30:48.784065Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5ae2-4d18-7921-a6f9-9ca09a337133
2026-02-14T07:30:48.804996Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-1e63-7422-8df1-29cc3cd854ed
2026-02-14T07:30:48.825715Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-2af1-7321-8d40-367f5a3ba03a
2026-02-14T07:30:48.846510Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-8eca-7cf3-8c60-d66e26ea0144
2026-02-14T07:30:48.867156Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-1935-7772-bf75-7eb9d084599e
2026-02-14T07:30:48.887953Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-45eb-7810-9be4-e9c813827907
2026-02-14T07:30:48.908736Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-5630-7b30-8723-45187528edea
2026-02-14T07:30:48.929536Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0a-f457-71d1-902a-d41b0df6fafa
2026-02-14T07:30:48.950401Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0a-f500-7013-80bc-cc4e70470657
2026-02-14T07:30:48.971224Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-1200-74e2-b68a-b5695adf8ddc
2026-02-14T07:30:48.992003Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-4f6c-79a1-ad3e-23dd8a997ea2
2026-02-14T07:30:49.012667Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e2-75e1-99f8-269a75536055
2026-02-14T07:30:49.033431Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e0-7850-aab6-44bd39f1876c
2026-02-14T07:30:49.054232Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e3-7490-b15b-7731fbbd70ff
2026-02-14T07:30:49.075039Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0e-b4b5-7fe2-a3e5-58d9a3aefdc9
2026-02-14T07:30:49.095871Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0e-b66a-79c1-a388-4af5a76df995
2026-02-14T07:30:49.116569Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0e-ef2a-7fe1-acb9-0efdd7098be1
2026-02-14T07:30:49.137460Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0f-1210-7683-86d6-0b2317ac7328
2026-02-14T07:30:49.158239Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0f-1b55-7231-b650-1e96b003c19f
mcp: surrealdb ready
mcp: playwright ready
mcp: exa ready
mcp startup: ready: surrealdb, playwright, exa

thinking
**Planning web search for docs**
🌐 Searching the web...
🌐 Searched: Weights & Biases Inference API grammar constrained decoding regex CFG documentation

thinking
**Opening official streaming docs**
🌐 Searching the web...
🌐 Searched: https://weave-docs.wandb.ai/reference/service-api/inference-post-inference-v-1-path-post/

thinking
**Locating inference documentation**
🌐 Searching the web...
🌐 Searched: https://docs.wandb.ai/inference

thinking
**Planning multiple API exploration**
🌐 Searching the web...
🌐 Searched: https://docs.wandb.ai/inference/response-settings/structured-output

thinking
**Checking detailed response format**
🌐 Searching the web...
🌐 Searched: https://docs.wandb.ai/inference/api-reference/chat-completions

thinking
**Evaluating grammar support options**
🌐 Searching the web...
🌐 Searched: site:docs.wandb.ai inference grammar regex CFG constrained decoding
🌐 Searching the web...
🌐 Searched: https://docs.wandb.ai/training/api-reference/chat-completions/create-chat-completion-1

thinking
**Clarifying API provider purpose**
🌐 Searching the web...
🌐 Searched: https://docs.wandb.ai/inference/api-reference

thinking
**Clarifying streaming schema constraints**
🌐 Searching the web...
🌐 Searched: site:docs.wandb.ai/inference guided_grammar

thinking
**Reviewing official WandB inference docs**
🌐 Searching the web...
🌐 Searched: site:docs.wandb.ai/inference/api-reference/chat-completions/create-chat-completion

thinking
**Inspecting response format schema**
🌐 Searching the web...
🌐 Searched: https://docs.wandb.ai/weave/reference/service-api/inference/inference-post

thinking
**Clarifying API doc scope**
codex
## Provider
**W&B Inference** (`https://api.inference.wandb.ai/v1`), documented as an **OpenAI-compatible** Chat Completions API.

## Grammar capability
- **Documented support:** schema-constrained output via `response_format.type = "json_schema"`.
- **Not documented in W&B Inference docs:** direct CFG grammar strings or regex-constrained decoding request params (e.g., no documented `guided_grammar`/`guided_regex` in Inference pages).

## Request shape
Use Chat Completions with:
```json
{
  "model": "...",
  "messages": [...],
  "response_format": {
    "type": "json_schema",
    "json_schema": {
      "name": "YourSchemaName",
      "strict": true,
      "schema": { "...": "JSON Schema object" }
    }
  },
  "stream": true
}
```
Key constrained-output fields are:
- `response_format.type`
- `response_format.json_schema.name`
- `response_format.json_schema.strict`
- `response_format.json_schema.schema`

## Grammar dialect and caveats
- Dialect is effectively **JSON Schema-based structured output** (not an exposed CFG/regex DSL in Inference docs).
- W&B positions this as preferred over JSON mode for schema adherence.
- Because it is OpenAI-compatible, behavior is framed as OpenAI-format structured output rather than a custom grammar engine.

## Streaming fields
For streaming (`stream: true`), W&B examples show:
- token chunks via `chunk.choices[0].delta.content`
- plus usage-style chunk(s) where `chunk.choices` may be empty (example comment: “Show CompletionUsage object”)

Relevant completion fields (non-stream example) remain OpenAI-style:
- `choices[].message.content`
- `choices[].finish_reason`
- `usage.*`

## Sources (URLs)
- https://docs.wandb.ai/inference  
- https://docs.wandb.ai/inference/api-reference  
- https://docs.wandb.ai/inference/api-reference/chat-completions  
- https://docs.wandb.ai/inference/response-settings/structured-output  
- https://docs.wandb.ai/inference/response-settings/streaming  
- (Contrast, different product/API): https://docs.wandb.ai/training/api-reference/chat-completions/create-chat-completion-1
tokens used
35,418
```

