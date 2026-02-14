# OpenRouter Provider Grammar Capability Cache

- Generated at: `2026-02-14T05:12:36.841661+00:00`
- API base: `https://openrouter.ai/api/v1`
- Models: `qwen/qwen3-coder-30b-a3b-instruct, qwen/qwen3-coder, qwen/qwen3-14b`
- Formats: `ll-lark, gbnf`

## Provider Summary

| Provider | Supports Grammar | Recommended Format | Obeys | Ignores | Reject |
|---|---:|---|---:|---:|---:|
| Alibaba | no |  | 0 | 0 | 6 |
| Amazon Bedrock | no |  | 0 | 0 | 2 |
| AtlasCloud | no |  | 0 | 0 | 2 |
| Chutes | no |  | 0 | 0 | 2 |
| DeepInfra | no |  | 0 | 0 | 4 |
| Google | no |  | 0 | 2 | 0 |
| Hyperbolic | no |  | 0 | 0 | 2 |
| Nebius | no |  | 0 | 0 | 4 |
| NextBit | no |  | 0 | 0 | 2 |
| Novita | no |  | 0 | 0 | 4 |
| SiliconFlow | no |  | 0 | 0 | 4 |
| Together | no |  | 0 | 0 | 2 |
| WandB | no |  | 0 | 0 | 2 |

## Raw Results

| Model | Provider | Format | Outcome | HTTP | Generated | Detail |
|---|---|---|---|---:|---|---|
| qwen/qwen3-coder-30b-a3b-instruct | Novita | ll-lark | reject | 502 |  | provider rejected grammar request: Provider returned error |
| qwen/qwen3-coder-30b-a3b-instruct | Novita | gbnf | reject | 502 |  | provider rejected grammar request: Provider returned error |
| qwen/qwen3-coder-30b-a3b-instruct | SiliconFlow | ll-lark | reject | 404 |  | provider rejected grammar request: No endpoints found for qwen/qwen3-coder-30b-a3b-instruct. |
| qwen/qwen3-coder-30b-a3b-instruct | SiliconFlow | gbnf | reject | 404 |  | provider rejected grammar request: No endpoints found for qwen/qwen3-coder-30b-a3b-instruct. |
| qwen/qwen3-coder-30b-a3b-instruct | Nebius | ll-lark | reject | 422 |  | provider rejected grammar request: Provider returned error |
| qwen/qwen3-coder-30b-a3b-instruct | Nebius | gbnf | reject | 422 |  | provider rejected grammar request: Provider returned error |
| qwen/qwen3-coder-30b-a3b-instruct | Amazon Bedrock | ll-lark | reject | 404 |  | provider rejected grammar request: No endpoints found for qwen/qwen3-coder-30b-a3b-instruct. |
| qwen/qwen3-coder-30b-a3b-instruct | Amazon Bedrock | gbnf | reject | 404 |  | provider rejected grammar request: No endpoints found for qwen/qwen3-coder-30b-a3b-instruct. |
| qwen/qwen3-coder-30b-a3b-instruct | Alibaba | ll-lark | reject | 200 |  | provider rejected grammar request: Upstream error from Alibaba: <400> InternalError.Algo.InvalidParameter: 'response_format.type' Invalid value: 'grammar'. Supported values are: 'json_object' and 'text'. |
| qwen/qwen3-coder-30b-a3b-instruct | Alibaba | gbnf | reject | 200 |  | provider rejected grammar request: Upstream error from Alibaba: <400> InternalError.Algo.InvalidParameter: 'response_format.type' Invalid value: 'grammar'. Supported values are: 'json_object' and 'text'. |
| qwen/qwen3-coder | DeepInfra | ll-lark | reject | 422 |  | provider rejected grammar request: Provider returned error |
| qwen/qwen3-coder | DeepInfra | gbnf | reject | 422 |  | provider rejected grammar request: Provider returned error |
| qwen/qwen3-coder | Google | ll-lark | accepts+ignores | 200 |  | provider accepted request but returned empty/non-text output |
| qwen/qwen3-coder | Google | gbnf | accepts+ignores | 200 |  | provider accepted request but returned empty/non-text output |
| qwen/qwen3-coder | SiliconFlow | ll-lark | reject | 404 |  | provider rejected grammar request: No endpoints found for qwen/qwen3-coder. |
| qwen/qwen3-coder | SiliconFlow | gbnf | reject | 404 |  | provider rejected grammar request: No endpoints found for qwen/qwen3-coder. |
| qwen/qwen3-coder | Novita | ll-lark | reject | 502 |  | provider rejected grammar request: Provider returned error |
| qwen/qwen3-coder | Novita | gbnf | reject | 502 |  | provider rejected grammar request: Provider returned error |
| qwen/qwen3-coder | Nebius | ll-lark | reject | 422 |  | provider rejected grammar request: Provider returned error |
| qwen/qwen3-coder | Nebius | gbnf | reject | 422 |  | provider rejected grammar request: Provider returned error |
| qwen/qwen3-coder | AtlasCloud | ll-lark | reject | 404 |  | provider rejected grammar request: No endpoints found for qwen/qwen3-coder. |
| qwen/qwen3-coder | AtlasCloud | gbnf | reject | 404 |  | provider rejected grammar request: No endpoints found for qwen/qwen3-coder. |
| qwen/qwen3-coder | Alibaba | ll-lark | reject | 400 |  | provider rejected grammar request: Provider returned error |
| qwen/qwen3-coder | Alibaba | gbnf | reject | 400 |  | provider rejected grammar request: Provider returned error |
| qwen/qwen3-coder | WandB | ll-lark | reject | 400 |  | provider rejected grammar request: Provider returned error |
| qwen/qwen3-coder | WandB | gbnf | reject | 400 |  | provider rejected grammar request: Provider returned error |
| qwen/qwen3-coder | Hyperbolic | ll-lark | reject | 404 |  | provider rejected grammar request: No endpoints found for qwen/qwen3-coder. |
| qwen/qwen3-coder | Hyperbolic | gbnf | reject | 404 |  | provider rejected grammar request: No endpoints found for qwen/qwen3-coder. |
| qwen/qwen3-coder | Together | ll-lark | reject | 404 |  | provider rejected grammar request: No endpoints found for qwen/qwen3-coder. |
| qwen/qwen3-coder | Together | gbnf | reject | 404 |  | provider rejected grammar request: No endpoints found for qwen/qwen3-coder. |
| qwen/qwen3-14b | Chutes | ll-lark | reject | 404 |  | provider rejected grammar request: No endpoints found for qwen/qwen3-14b. |
| qwen/qwen3-14b | Chutes | gbnf | reject | 404 |  | provider rejected grammar request: No endpoints found for qwen/qwen3-14b. |
| qwen/qwen3-14b | NextBit | ll-lark | reject | 200 |  | provider rejected grammar request: JSON error injected into SSE stream |
| qwen/qwen3-14b | NextBit | gbnf | reject | 200 |  | provider rejected grammar request: JSON error injected into SSE stream |
| qwen/qwen3-14b | DeepInfra | ll-lark | reject | 422 |  | provider rejected grammar request: Provider returned error |
| qwen/qwen3-14b | DeepInfra | gbnf | reject | 422 |  | provider rejected grammar request: Provider returned error |
| qwen/qwen3-14b | Alibaba | ll-lark | reject | 400 |  | provider rejected grammar request: Provider returned error |
| qwen/qwen3-14b | Alibaba | gbnf | reject | 400 |  | provider rejected grammar request: Provider returned error |
