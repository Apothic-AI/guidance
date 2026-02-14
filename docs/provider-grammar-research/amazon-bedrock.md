## Provider
Amazon Bedrock (official AWS docs, current as of February 2026).

## Grammar capability
- **Yes, for JSON-schema-constrained generation** on Bedrock inference APIs (`Converse*`, `InvokeModel*`) via structured outputs.
- Bedrock states it **compiles schemas into grammars** and caches compiled grammars.
- **Direct regex/CFG-style constraints** are explicitly documented for **Custom Model Import (CMI)** OpenAI-style APIs via `structured_outputs` types: `json`, `regex`, `choice`, `grammar`.
- For standard Bedrock `Converse`/`InvokeModel` structured output, documented type is `json_schema` (plus strict tool schema validation).

## Request shape
- **Converse / ConverseStream**
  - `outputConfig.textFormat.type = "json_schema"`
  - `outputConfig.textFormat.structure.jsonSchema` (with `schema`, optional `name`, `description`)
  - Tool strictness: `toolConfig.tools[].toolSpec.strict = true`
- **InvokeModel (Anthropic Claude format)**
  - `output_config.format.type = "json_schema"`
  - `output_config.format.schema = {...}`
  - Tool strictness: `tools[].strict = true`
- **InvokeModel (open-weight format)**
  - `response_format.type = "json_schema"`
  - `response_format.json_schema = { name, schema }`
- **Custom Model Import (imported models, OpenAI/Bedrock completion variants)**
  - `response_format` supports `json_object | json_schema`
  - `structured_outputs` supports `json | regex | choice | grammar`

## Grammar dialect and caveats
- Bedrock structured outputs validate against a **supported subset of JSON Schema Draft 2020-12**.
- AWS docs do **not specify a formal grammar dialect name** (for `structured_outputs.grammar`) nor regex engine flavor in the cited pages.
- Caveats called out by AWS:
  - First use of a new schema may add latency (grammar compilation).
  - Compiled grammars are cached for 24h.
  - Structured outputs can increase latency/throughput cost, especially complex schemas/grammar.
  - For Anthropic on Bedrock, structured outputs are incompatible with citations (400 error if combined).

## Streaming fields
- **ConverseStream** emits ordered events:
  - `messageStart`
  - `contentBlockStart`
  - `contentBlockDelta` (delta can include `text`, `reasoningContent`, `toolUse`, etc.)
  - `contentBlockStop`
  - `messageStop` (includes `stopReason`, optional `additionalModelResponseFields`)
  - `metadata` (`usage`, `metrics`, etc.)
- **InvokeModelWithResponseStream** returns stream chunks under `chunk.bytes` (payload format remains model-specific).  
- No special dedicated “grammar status” streaming field is documented in these references.

## Sources (URLs)
- https://docs.aws.amazon.com/bedrock/latest/userguide/structured-output.html
- https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html
- https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_OutputConfig.html
- https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_OutputFormat.html
- https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_OutputFormatStructure.html
- https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_JsonSchemaDefinition.html
- https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ContentBlockDelta.html
- https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_MessageStopEvent.html
- https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/custom-model-import-advanced-features.html

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
session id: 019c5b0c-fd96-7c40-9fb5-4533f503a218
--------
user
Research official documentation for provider "Amazon Bedrock" focused on grammar-constrained generation.
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
2026-02-14T07:28:24.015322Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5531-6c60-7612-b81c-b02333263b22
2026-02-14T07:28:24.054832Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5080-050b-7c53-92a8-9c52ce325359
2026-02-14T07:28:24.080834Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c58f2-9999-7e13-8897-cb3cb6765c62
2026-02-14T07:28:24.107613Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5ae2-4d18-7921-a6f9-9ca09a337133
2026-02-14T07:28:24.133238Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-1e63-7422-8df1-29cc3cd854ed
2026-02-14T07:28:24.167696Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-2af1-7321-8d40-367f5a3ba03a
2026-02-14T07:28:24.186042Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-8eca-7cf3-8c60-d66e26ea0144
2026-02-14T07:28:24.210359Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-1935-7772-bf75-7eb9d084599e
2026-02-14T07:28:24.246360Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-45eb-7810-9be4-e9c813827907
2026-02-14T07:28:24.271806Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-5630-7b30-8723-45187528edea
2026-02-14T07:28:24.314053Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0a-f457-71d1-902a-d41b0df6fafa
2026-02-14T07:28:24.347167Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0a-f500-7013-80bc-cc4e70470657
2026-02-14T07:28:24.392952Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-1200-74e2-b68a-b5695adf8ddc
2026-02-14T07:28:24.423375Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-4f6c-79a1-ad3e-23dd8a997ea2
2026-02-14T07:28:24.435032Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e2-75e1-99f8-269a75536055
2026-02-14T07:28:24.472132Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e0-7850-aab6-44bd39f1876c
2026-02-14T07:28:24.498178Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e3-7490-b15b-7731fbbd70ff
mcp: surrealdb ready
mcp: playwright ready
mcp: exa ready
mcp startup: ready: surrealdb, playwright, exa

thinking
**Planning web search on Bedrock features**
🌐 Searching the web...
🌐 Searched: site:docs.aws.amazon.com Amazon Bedrock grammar constrained decoding CFG regex

thinking
**Gathering request field details**
🌐 Searching the web...
🌐 Searched: https://docs.aws.amazon.com/bedrock/latest/userguide/structured-output.html

thinking
**Inspecting grammar regex context**
🌐 Searching the web...
🌐 Searched: 'structured_outputs' in https://docs.aws.amazon.com/bedrock/latest/userguide/custom-model-import-advanced-features.html

thinking
**Checking outputConfig field location**
🌐 Searching the web...
🌐 Searched: 'outputConfig' in https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference-call.html

thinking
**Reviewing grammar example context**
🌐 Searching the web...
🌐 Searched: https://docs.aws.amazon.com/bedrock/latest/userguide/custom-model-import-advanced-features.html

thinking
**Searching docs for grammar schema**
🌐 Searching the web...
🌐 Searched: site:docs.aws.amazon.com bedrock structured_outputs grammar dialect

thinking
**Assessing response field needs**
🌐 Searching the web...
🌐 Searched: 'EBNF' in https://docs.aws.amazon.com/bedrock/latest/userguide/custom-model-import-advanced-features.html

thinking
**Scoping API outputConfig details**
🌐 Searching the web...
🌐 Searched: site:docs.aws.amazon.com bedrock TextFormat outputConfig textFormat ConverseStream

thinking
**Planning output format research**
🌐 Searching the web...
🌐 Searched: https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html

thinking
**Identifying output format docs**
🌐 Searching the web...
🌐 Searched: https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_OutputConfig.html

thinking
**Considering union fields for content block delta**
🌐 Searching the web...
🌐 Searched: https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ContentBlockDelta.html

thinking
**Identifying output format details**
🌐 Searching the web...
🌐 Searched: https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_OutputFormatStructure.html

thinking
**Clarifying model fields and streaming support**
codex
## Provider
Amazon Bedrock (official AWS docs, current as of February 2026).

## Grammar capability
- **Yes, for JSON-schema-constrained generation** on Bedrock inference APIs (`Converse*`, `InvokeModel*`) via structured outputs.
- Bedrock states it **compiles schemas into grammars** and caches compiled grammars.
- **Direct regex/CFG-style constraints** are explicitly documented for **Custom Model Import (CMI)** OpenAI-style APIs via `structured_outputs` types: `json`, `regex`, `choice`, `grammar`.
- For standard Bedrock `Converse`/`InvokeModel` structured output, documented type is `json_schema` (plus strict tool schema validation).

## Request shape
- **Converse / ConverseStream**
  - `outputConfig.textFormat.type = "json_schema"`
  - `outputConfig.textFormat.structure.jsonSchema` (with `schema`, optional `name`, `description`)
  - Tool strictness: `toolConfig.tools[].toolSpec.strict = true`
- **InvokeModel (Anthropic Claude format)**
  - `output_config.format.type = "json_schema"`
  - `output_config.format.schema = {...}`
  - Tool strictness: `tools[].strict = true`
- **InvokeModel (open-weight format)**
  - `response_format.type = "json_schema"`
  - `response_format.json_schema = { name, schema }`
- **Custom Model Import (imported models, OpenAI/Bedrock completion variants)**
  - `response_format` supports `json_object | json_schema`
  - `structured_outputs` supports `json | regex | choice | grammar`

## Grammar dialect and caveats
- Bedrock structured outputs validate against a **supported subset of JSON Schema Draft 2020-12**.
- AWS docs do **not specify a formal grammar dialect name** (for `structured_outputs.grammar`) nor regex engine flavor in the cited pages.
- Caveats called out by AWS:
  - First use of a new schema may add latency (grammar compilation).
  - Compiled grammars are cached for 24h.
  - Structured outputs can increase latency/throughput cost, especially complex schemas/grammar.
  - For Anthropic on Bedrock, structured outputs are incompatible with citations (400 error if combined).

## Streaming fields
- **ConverseStream** emits ordered events:
  - `messageStart`
  - `contentBlockStart`
  - `contentBlockDelta` (delta can include `text`, `reasoningContent`, `toolUse`, etc.)
  - `contentBlockStop`
  - `messageStop` (includes `stopReason`, optional `additionalModelResponseFields`)
  - `metadata` (`usage`, `metrics`, etc.)
- **InvokeModelWithResponseStream** returns stream chunks under `chunk.bytes` (payload format remains model-specific).  
- No special dedicated “grammar status” streaming field is documented in these references.

## Sources (URLs)
- https://docs.aws.amazon.com/bedrock/latest/userguide/structured-output.html
- https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html
- https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_OutputConfig.html
- https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_OutputFormat.html
- https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_OutputFormatStructure.html
- https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_JsonSchemaDefinition.html
- https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ContentBlockDelta.html
- https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_MessageStopEvent.html
- https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/custom-model-import-advanced-features.html
tokens used
46,345
```

