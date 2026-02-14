# Provider Grammar Docs Matrix

- Source corpus: `docs/provider-grammar-research/*.md`
- Scope: documented provider-native constrained output features (not OpenRouter runtime behavior)

| Provider | Support | Dialect | Request Shape | Streaming Fields | Source |
|---|---|---|---|---|---|
| Alibaba | json_schema_only | none | response_format.json_object|json_schema | choices[].delta.content | `docs/provider-grammar-research/alibaba.md` |
| Amazon Bedrock | json_schema_plus_provider_specific | provider_specific_cmi | outputConfig.textFormat / structured_outputs (CMI) | contentBlockDelta.text|reasoningContent (ConverseStream) | `docs/provider-grammar-research/amazon-bedrock.md` |
| AtlasCloud | none_documented | none | no documented response_format grammar fields | SSE deltas documented, schema unspecified | `docs/provider-grammar-research/atlascloud.md` |
| Chutes | regex_plus_json_guided | none_documented_cfg | guided_json (vLLM), regex in SGLang | choices[].delta.content | `docs/provider-grammar-research/chutes.md` |
| DeepInfra | json_schema_only | none | response_format.json_object|json_schema | choices[].delta.content | `docs/provider-grammar-research/deepinfra.md` |
| Fireworks | grammar_string | gbnf | response_format={type:"grammar",grammar:"..."} | choices[].delta.content (and reasoning_content seen in practice) | `docs/provider-grammar-research/fireworks.md` |
| Friendli | regex_plus_json_schema | regex | response_format.type=json_schema|json_object|regex | choices[].delta.content | `docs/provider-grammar-research/friendli.md` |
| GMICloud | json_object_only | none | response_format.type=json_object | usage in final stream chunk | `docs/provider-grammar-research/gmicloud.md` |
| Google | json_schema_only | none | generationConfig.responseSchema/responseJsonSchema | candidates[].content.parts[].text | `docs/provider-grammar-research/google.md` |
| Hyperbolic | none_documented | none | no documented constrained-decoding request fields | choices[].delta.content | `docs/provider-grammar-research/hyperbolic.md` |
| Nebius | json_schema_only | none | response_format json_object/json_schema (doc inconsistency) | SSE + [DONE], chunk schema sparse | `docs/provider-grammar-research/nebius.md` |
| NextBit | json_schema_via_openrouter | none | OpenRouter response_format json_object/json_schema | choices[].delta.content, finish_reason, usage | `docs/provider-grammar-research/nextbit.md` |
| Novita | json_schema_only | none | response_format.type=json_schema|json_object | SSE + [DONE] | `docs/provider-grammar-research/novita.md` |
| Parasail | regex_plus_json_schema | regex | structured_output (json schema or regex), guided_json | OpenAI-compatible deltas | `docs/provider-grammar-research/parasail.md` |
| Phala | json_schema_only | none | response_format.type=json_schema | choices[].delta.content + [DONE] | `docs/provider-grammar-research/phala.md` |
| SiliconFlow | json_object_plus_tool_schema | none | response_format.json_object and tools[].function.strict | delta.content + delta.reasoning_content | `docs/provider-grammar-research/siliconflow.md` |
| Together | regex_plus_json_schema | regex | response_format.type=json_schema|regex | delta.content (+ reasoning for some models) | `docs/provider-grammar-research/together.md` |
| Venice | json_schema_only | none | response_format.type=json_schema | delta.content (chat), typed SSE events in /responses | `docs/provider-grammar-research/venice.md` |
| WandB | json_schema_only | none | response_format.type=json_schema | chunk.choices[0].delta.content | `docs/provider-grammar-research/wandb.md` |
| Z.AI | json_object_only | none | response_format.type=json_object | delta.content + delta.reasoning_content | `docs/provider-grammar-research/z-ai.md` |

JSON: `docs/provider-grammar-research-matrix.json`
