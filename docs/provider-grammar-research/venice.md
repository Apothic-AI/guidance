## Provider
**Venice.ai** (`/api/v1/chat/completions`, plus Alpha `/responses` API).

## Grammar capability
- **No documented CFG/BNF/regex-constrained decoding API** (no `grammar`, `cfg`, or `regex` request field in official OpenAPI for chat/responses).
- Venice documents **structured output via JSON Schema** using `response_format.type = "json_schema"`.

## Request shape
For Chat Completions:
```json
{
  "model": "…",
  "messages": [...],
  "response_format": {
    "type": "json_schema",
    "json_schema": { "type": "object", "properties": { ... } }
  },
  "stream": true,
  "stream_options": { "include_usage": true }
}
```
Also supported (legacy):  
`"response_format": { "type": "json_object" }` (documented as deprecated).

## Grammar dialect and caveats
- Dialect is **JSON Schema-based structured outputs** (not CFG grammar text).
- Venice docs describe this as a **subset/compatibility-style structured output path** and recommend models that support response schemas (model capability flag surfaced in model metadata/docs).
- Practical caveat: if you need true grammar/regex decoding semantics (token-level CFG control), Venice docs do not expose a dedicated field for that; only JSON-schema-constrained object generation is documented.

## Streaming fields
Chat Completions request-side fields relevant to constrained output:
- `stream: boolean`
- `stream_options.include_usage: boolean`
- `venice_parameters.include_search_results_in_stream: boolean` (Venice-specific; first emitted chunk for search results)

Responses API streaming (SSE) docs list typed events, including:
- `response.output_text.delta`
- `response.output_text.done`
- `response.completed`
- `response.failed`

These are the stream events you’d use when consuming constrained/structured output progressively.

## Sources (URLs)
- https://docs.venice.ai/guides/structured-responses
- https://docs.venice.ai/guides/streaming
- https://api.venice.ai/doc/api/swagger.yaml
- https://docs.venice.ai/api-reference/endpoint/chat/completions

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
session id: 019c5b0f-1b55-7231-b650-1e96b003c19f
--------
user
Research official documentation for provider "Venice" focused on grammar-constrained generation.
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
2026-02-14T07:30:42.669554Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5531-6c60-7612-b81c-b02333263b22
2026-02-14T07:30:42.690732Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5080-050b-7c53-92a8-9c52ce325359
2026-02-14T07:30:42.711617Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c58f2-9999-7e13-8897-cb3cb6765c62
2026-02-14T07:30:42.732410Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5ae2-4d18-7921-a6f9-9ca09a337133
2026-02-14T07:30:42.753117Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-1e63-7422-8df1-29cc3cd854ed
2026-02-14T07:30:42.773998Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-2af1-7321-8d40-367f5a3ba03a
2026-02-14T07:30:42.794807Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b06-8eca-7cf3-8c60-d66e26ea0144
2026-02-14T07:30:42.815585Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-1935-7772-bf75-7eb9d084599e
2026-02-14T07:30:42.836245Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-45eb-7810-9be4-e9c813827907
2026-02-14T07:30:42.857160Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b07-5630-7b30-8723-45187528edea
2026-02-14T07:30:42.878505Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0a-f457-71d1-902a-d41b0df6fafa
2026-02-14T07:30:42.899237Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0a-f500-7013-80bc-cc4e70470657
2026-02-14T07:30:42.919948Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-1200-74e2-b68a-b5695adf8ddc
2026-02-14T07:30:42.940596Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-4f6c-79a1-ad3e-23dd8a997ea2
2026-02-14T07:30:42.961215Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e2-75e1-99f8-269a75536055
2026-02-14T07:30:42.981972Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e0-7850-aab6-44bd39f1876c
2026-02-14T07:30:43.002745Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0c-61e3-7490-b15b-7731fbbd70ff
2026-02-14T07:30:43.023665Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0e-4762-75c1-b6a7-713ce89707a2
2026-02-14T07:30:43.044794Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0e-b4b5-7fe2-a3e5-58d9a3aefdc9
2026-02-14T07:30:43.065615Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0e-b66a-79c1-a388-4af5a76df995
2026-02-14T07:30:43.086238Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0e-ef2a-7fe1-acb9-0efdd7098be1
2026-02-14T07:30:43.107082Z ERROR codex_core::rollout::list: state db missing rollout path for thread 019c5b0f-1210-7683-86d6-0b2317ac7328
mcp: surrealdb ready
mcp: playwright ready
mcp: exa ready
mcp startup: ready: surrealdb, playwright, exa

thinking
**Planning targeted web search**
🌐 Searching the web...
🌐 Searched: Venice API documentation grammar constrained generation CFG regex

thinking
**Checking official API docs**
🌐 Searching the web...
🌐 Searched: https://adamxchen.github.io/venice/docs/user_guide

thinking
**Locating correct API docs**
🌐 Searching the web...
🌐 Searched: site:docs.venice.ai API chat completions grammar regex

thinking
**Exploring response format support**
codex
Researching Venice’s official API docs now, focusing on `response_format` and chat-completions schema to confirm whether grammar/CFG/regex constrained decoding is actually supported and what fields are available.
🌐 Searching the web...
🌐 Searched: https://docs.venice.ai/welcome/guides/structured-responses

thinking
**Searching docs for grammar mentions**
🌐 Searching the web...
🌐 Searched: 'grammar' in https://docs.venice.ai/api-reference/endpoint/chat/completions

thinking
**Investigating streaming endpoint**
codex
I confirmed `response_format` is present and there’s no explicit `grammar`/`regex`/`cfg` field on the main Chat Completions schema. Next I’m checking the dedicated streaming endpoint/spec to capture streaming response fields accurately.
🌐 Searching the web...
🌐 Searched: site:docs.venice.ai "Streaming" "chat/completions" "api-reference/endpoint"

thinking
**Searching OpenAPI spec URL**
🌐 Searching the web...
🌐 Searched: 'openapi' in https://docs.venice.ai/api-reference/api-spec

thinking
**Assessing streaming field sources**
codex
I found the core constraints details in `Structured Responses` and `Chat Completions`; now I’m verifying model capability flags and any explicit streaming-chunk fields before I finalize.
🌐 Searching the web...
🌐 Searched: site:docs.venice.ai supportsResponseSchema models endpoint

thinking
**Identifying relevant API endpoints**
🌐 Searching the web...
🌐 Searched: site:docs.venice.ai "include_search_results_in_stream"

thinking
**Inspecting streaming response fields**
codex
I located Venice’s published Swagger file URL; I’m pulling it now to extract exact streaming schema fields instead of inferring from OpenAI compatibility claims.
🌐 Searching the web...
🌐 Searched the web

thinking
**Switching to curl for fetch**
codex
The browser fetch for `swagger.yaml` failed, so I’m switching to `curl` in the terminal to read the official schema directly and extract streaming/chunk fields.
exec
/usr/bin/zsh -lc 'curl -sSL https://api.venice.ai/doc/api/swagger.yaml | head -n 140' in /home/bitnom/Code/apothic-monorepo/libs/python/guidance succeeded in 358ms:
externalDocs:
  description: Venice.ai API documentation
  url: https://docs.venice.ai
info:
  description: The Venice.ai API.
  termsOfService: https://venice.ai/legal/tos
  title: Venice.ai API
  version: "20260211.074006"
openapi: 3.0.0
security:
  - BearerAuth: []
servers:
  - url: https://api.venice.ai/api/v1
tags:
  - description: Transcribe audio using AI models.
    name: Audio
  - description: Given a list of messages comprising a conversation, the model will
      return a response. Supports multimodal inputs including text, images,
      audio (input_audio), and video (video_url) for compatible models.
    name: Chat

thinking
**Planning pattern search with curl and ripgrep**
exec
/usr/bin/zsh -lc 'tmp=$(mktemp); curl -sSL https://api.venice.ai/doc/api/swagger.yaml -o "$tmp"; echo $tmp; rg -n "grammar|cfg|regex|response_format|json_schema|stream|delta|ChatCompletionChunk|include_search_results_in_stream|include_usage|response'"\\.output\" \""'$tmp" | head -n 200' in /home/bitnom/Code/apothic-monorepo/libs/python/guidance succeeded in 481ms:
/tmp/user/1000/tmp.JeevBKPs7d
709:        stream:
711:          description: Whether to stream back partial progress. Defaults to false.
713:        stream_options:
716:            include_usage:
718:              description: Whether to include usage information in the stream.
781:                first chunk of a streaming result, or in the non streaming
796:            include_search_results_in_stream:
800:                search results in the stream as the first emitted chunk.
819:        response_format:
823:                json_schema:
830:                    - json_schema
832:                - json_schema
838:                json_schema:
848:                type: json_schema
849:              title: json_schema
860:                deprecated implementation and the preferred use is json_schema.
1530:        stream:
1532:          description: Whether to stream back partial progress.
1555:            include_search_results_in_stream:

thinking
**Inspecting schema context**
exec
/usr/bin/zsh -lc "tmp=/tmp/user/1000/tmp.JeevBKPs7d; sed -n '680,900p' \""'$tmp"' in /home/bitnom/Code/apothic-monorepo/libs/python/guidance succeeded in 51ms:
        seed:
          type: integer
          minimum: 0
          exclusiveMinimum: true
          description: The random seed used to generate the response. This is useful for
            reproducibility.
          example: 42
        stop:
          anyOf:
            - type: string
              title: String
            - type: array
              items:
                type: string
              minItems: 1
              maxItems: 4
              title: Array of Strings
            - nullable: true
              title: "null"
          description: Up to 4 sequences where the API will stop generating further

thinking
**Identifying streaming response schema location**
exec
/usr/bin/zsh -lc "tmp=/tmp/user/1000/tmp.JeevBKPs7d; sed -n '3560,4230p' \""'$tmp"' in /home/bitnom/Code/apothic-monorepo/libs/python/guidance succeeded in 50ms:
              usd: 0.6
              diem: 0.6
          traits:
            - fastest
        object: model
        owned_by: venice.ai
        type: text
    ModelTraitSchema:
      type: object
      additionalProperties:
        type: string
      description: List of available models
      example:
        default: zai-org-glm-4.7
        fastest: qwen3-4b
    ModelCompatibilitySchema:
      type: object
      additionalProperties:
        type: string
      description: List of available models

thinking
**Searching streaming chunk schema**
codex
I’ve extracted the request-side fields from the official schema. I’m now pinpointing the SSE/chunk object definitions (`chat.completion.chunk`/Responses stream events) so I can list the exact streaming fields that matter for constrained output.
exec
/usr/bin/zsh -lc "tmp=/tmp/user/1000/tmp.JeevBKPs7d; rg -n \"chat\\.completion\\.chunk|delta|choices:|object: chat\\.completion|data:|event:|ResponseStream|response\\.output|output_text|json_schema\" \""'$tmp" | head -n 240' in /home/bitnom/Code/apothic-monorepo/libs/python/guidance succeeded in 51ms:
227:                                    data:
262:                                  data: <base64-encoded-audio>
300:                                        data:video/mp4;base64,...). Supported
397:                        data:
823:                json_schema:
830:                    - json_schema
832:                - json_schema
838:                json_schema:
848:                type: json_schema
849:              title: json_schema
860:                deprecated implementation and the preferred use is json_schema.
958:            data:
993:          data: <base64-encoded-audio>
1031:                data:video/mp4;base64,...). Supported formats: mp4, mpeg, mov,
1120:                                        - output_text
1199:                                            - output_text
1638:                            - output_text
1777:        embed_exif_metadata:
2537:            "https://") or a data URL (starting with "data:").
2538:          example: data:image/png;base64,iVBORw0K...



thinking
**Investigating streaming examples source**
thinking
**Planning API endpoint streaming**
thinking
**Identifying API endpoint details**
🌐 Searching the web...
🌐 Searched the web
🌐 Searching the web...
🌐 Searched the web

thinking
**Planning unified search and open**
🌐 Searching the web...
🌐 Searched: site:docs.venice.ai chat completions stream options include_usage

thinking
**Planning response schema support**
🌐 Searching the web...
🌐 Searched: site:docs.venice.ai supportsResponseSchema models endpoint

thinking
**Identifying streaming schema details**
codex
I couldn’t find chunk fields in the top-level chat endpoint docs page, so I’m extracting them from the OpenAPI file by searching for SSE event schemas and `response.*` stream event names.
exec
/usr/bin/zsh -lc "tmp=/tmp/user/1000/tmp.JeevBKPs7d; rg -n \"\\bdelta\\b|chat\\.completion\\.chunk|object:\\s*"'$|event'"\\.|response\\.completed|response\\.output_text|Server-Sent|text/event-stream|\\[DONE\\]\" \""'$tmp" | head -n 300' in /home/bitnom/Code/apothic-monorepo/libs/python/guidance succeeded in 51ms:
1571:        object:
3498:        object:
3867:                  object:
4181:        This endpoint supports streaming via Server-Sent Events when `stream:
4204:                  object:
4736:                  object:
5174:                  object:
5244:                  object:
5320:                  object:
5486:                  object:
6263:                  object:
6692:                  object:
6819:                  object:
6894:                        object:
6907:                  object:

thinking
**Planning schema inspection**
🌐 Searching the web...
🌐 Searched: site:api.venice.ai/doc/api/swagger.yaml response.output_text.delta Venice
exec
/usr/bin/zsh -lc "tmp=/tmp/user/1000/tmp.JeevBKPs7d; sed -n '6760,6955p' \""'$tmp"' in /home/bitnom/Code/apothic-monorepo/libs/python/guidance succeeded in 51ms:
                      shareUrl:
                        type: string
                        nullable: true
                        description: Share URL of the character
                        example: https://venice.ai/c/alan-watts
                      photoUrl:
                        type: string
                        nullable: true
                        description: URL of the character photo
                        example: https://outerface.venice.ai/api/characters/2f460055-7595-4640-9cb6-c442c4c869b0/photo
                      slug:
                        type: string
                        description: Slug of the character to be used in the completions API
                        example: alan-watts
                      stats:
                        type: object
                        properties:
                          imports:
                            type: number
                            description: Number of imports for the character

thinking
**Checking event schema region**
codex
I found the OpenAPI section offsets for stream event schemas; I’m inspecting those blocks now to identify the exact event names and payload fields used during streaming.
exec
/usr/bin/zsh -lc "tmp=/tmp/user/1000/tmp.JeevBKPs7d; sed -n '5080,5365p' \""'$tmp"' in /home/bitnom/Code/apothic-monorepo/libs/python/guidance succeeded in 50ms:
          description: OK - PNG image with transparent background
          content:
            image/png:
              schema:
                format: binary
                type: string
        "400":
          description: Invalid request parameters
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DetailedError"
        "401":
          description: Authentication failed
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StandardError"
        "402":
          description: Insufficient USD or Diem balance to complete request






thinking
**Searching for streaming docs**
thinking
**Noting need for stream event fields**
thinking
**Clarifying streaming schema requirements**
thinking
**Planning contextual line fetching**
thinking
**Inspecting schema keyword support**
thinking
**Preparing concise markdown with sources**
codex
## Provider
**Venice.ai** (`/api/v1/chat/completions`, plus Alpha `/responses` API).

## Grammar capability
- **No documented CFG/BNF/regex-constrained decoding API** (no `grammar`, `cfg`, or `regex` request field in official OpenAPI for chat/responses).
- Venice documents **structured output via JSON Schema** using `response_format.type = "json_schema"`.

## Request shape
For Chat Completions:
```json
{
  "model": "…",
  "messages": [...],
  "response_format": {
    "type": "json_schema",
    "json_schema": { "type": "object", "properties": { ... } }
  },
  "stream": true,
  "stream_options": { "include_usage": true }
}
```
Also supported (legacy):  
`"response_format": { "type": "json_object" }` (documented as deprecated).

## Grammar dialect and caveats
- Dialect is **JSON Schema-based structured outputs** (not CFG grammar text).
- Venice docs describe this as a **subset/compatibility-style structured output path** and recommend models that support response schemas (model capability flag surfaced in model metadata/docs).
- Practical caveat: if you need true grammar/regex decoding semantics (token-level CFG control), Venice docs do not expose a dedicated field for that; only JSON-schema-constrained object generation is documented.

## Streaming fields
Chat Completions request-side fields relevant to constrained output:
- `stream: boolean`
- `stream_options.include_usage: boolean`
- `venice_parameters.include_search_results_in_stream: boolean` (Venice-specific; first emitted chunk for search results)

Responses API streaming (SSE) docs list typed events, including:
- `response.output_text.delta`
- `response.output_text.done`
- `response.completed`
- `response.failed`

These are the stream events you’d use when consuming constrained/structured output progressively.

## Sources (URLs)
- https://docs.venice.ai/guides/structured-responses
- https://docs.venice.ai/guides/streaming
- https://api.venice.ai/doc/api/swagger.yaml
- https://docs.venice.ai/api-reference/endpoint/chat/completions
tokens used
58,295
```

