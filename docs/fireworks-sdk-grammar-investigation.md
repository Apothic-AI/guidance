# Fireworks SDK Grammar Investigation

## Metadata

- Status: current
- Last updated: 2026-02-14
- Scope: Fireworks grammar-mode request/stream behavior and Guidance integration implications

## Why This Exists

We observed constrained grammar runs on Fireworks where streaming text appeared in
`delta.reasoning_content` instead of `delta.content`. This document records what we verified in the Fireworks
SDK and live API probes.

## References

- Fireworks structured response formatting:
  - https://docs.fireworks.ai/structured-responses/structured-response-formatting.md
- Fireworks grammar-based outputs:
  - https://docs.fireworks.ai/structured-responses/structured-output-grammar-based.md
- Fireworks reasoning docs:
  - https://docs.fireworks.ai/guides/querying-text-models#reasoning-models

## SDK Findings (Fireworks Python SDK)

Inspected local package `fireworks-ai` (installed in the dev env):

- `fireworks/llm/_types.py`
  - defines `ResponseFormatGrammar` with:
    - `type: "grammar"`
    - `grammar: str`
- `fireworks/llm/chat_completion.py`
  - passes `response_format` through to chat-completions request payload.
- `fireworks/client/api.py`
  - chat chunk/message schema includes both:
    - `content`
    - `reasoning_content`

Takeaway: the SDK explicitly models `reasoning_content` as a first-class stream/message field and does not
abstract it away for us.

## Live Probe Findings

Date: 2026-02-14

1. Direct Fireworks API, grammar mode, streaming:
   - generated tokens arrived in `delta.reasoning_content`
   - `delta.content` stayed null
2. Direct Fireworks API, grammar mode, non-streaming:
   - final output appeared in `message.content`
3. OpenRouter routed to Fireworks (`provider.order=["fireworks"]`, `require_parameters=true`, `allow_fallbacks=false`):
   - grammar-mode stream emitted constrained tokens in `delta.content`
   - did not need `reasoning_content` fallback in this run

## Guidance Changes Based On Findings

1. Stream parser now supports grammar-mode fallback from `delta.content` to `delta.reasoning_content`:
   - enabled for direct Fireworks clients.
   - enabled for OpenRouter only when the streamed provider is Fireworks.
2. OpenRouter grammar path now applies stricter routing defaults for constrained calls:
   - `extra_body.provider.require_parameters = true` (default)
   - `extra_body.provider.allow_fallbacks = false` (default)
   - explicit user/provider settings are still respected.

## OpenRouter Implications

The Fireworks-specific handling is likely useful for OpenRouter provider routes that share the same backend
structured-decoding stack, but behavior is not guaranteed 1:1 across providers/routes.

Current stance:

- keep provider-aware parsing and fail-closed local validation,
- continue collecting route-level evidence before broadening fallback behavior.

