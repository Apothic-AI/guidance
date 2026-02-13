# OpenRouter Grammar Probe Matrix

- Generated at: `2026-02-13T10:52:46.524487+00:00`
- API base: `https://openrouter.ai/api/v1`
- Model: `z-ai/glm-5`

| Provider | Format | Outcome | HTTP | Generated | Detail |
|---|---|---|---:|---|---|
| AtlasCloud | ll-lark | accepts+ignores | 200 |  | provider accepted request but returned empty/non-text output |
| AtlasCloud | gbnf | reject | 429 |  | provider rejected grammar request: Provider returned error |
| AtlasCloud | minimal-lark | reject | 429 |  | provider rejected grammar request: Provider returned error |
| Friendli | ll-lark | reject | 400 |  | provider rejected grammar request: Provider returned error |
| Friendli | gbnf | reject | 400 |  | provider rejected grammar request: Provider returned error |
| Friendli | minimal-lark | reject | 400 |  | provider rejected grammar request: Provider returned error |
| GMICloud | ll-lark | reject | 422 |  | provider rejected grammar request: Provider returned error |
| GMICloud | gbnf | reject | 422 |  | provider rejected grammar request: Provider returned error |
| GMICloud | minimal-lark | reject | 422 |  | provider rejected grammar request: Provider returned error |
| Parasail | ll-lark | reject | 429 |  | provider rejected grammar request: Provider returned error |
| Parasail | gbnf | reject | 429 |  | provider rejected grammar request: Provider returned error |
| Parasail | minimal-lark | reject | 400 |  | provider rejected grammar request: Provider returned error |
| Venice | ll-lark | reject | 400 |  | provider rejected grammar request: Provider returned error |
| Venice | gbnf | reject | 400 |  | provider rejected grammar request: Provider returned error |
| Venice | minimal-lark | reject | 400 |  | provider rejected grammar request: Provider returned error |
| Novita | ll-lark | reject | 502 |  | provider rejected grammar request: Provider returned error |
| Novita | gbnf | reject | 502 |  | provider rejected grammar request: Provider returned error |
| Novita | minimal-lark | reject | 502 |  | provider rejected grammar request: Provider returned error |
