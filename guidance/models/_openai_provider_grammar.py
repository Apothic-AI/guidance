from __future__ import annotations

import time
from typing import Any, Iterator

from .._ast import GrammarNode, RegexNode
from .._schema import TokenUsage
from ..trace import OutputAttr, TextOutput, TokenOutput
from ._grammar_support import (
    ConstraintProviderRejectedError,
    ConstraintUnsupportedFeatureError,
    FireworksGBNFBuilder,
    OpenAIResponsesGrammarBuilder,
    apply_local_constraint_validation,
    looks_like_provider_rejection_error,
)
from ._openai_base import AudioContent, BaseOpenAIInterpreter, ContentMessage, ImageUrlContent, TextContent


class OpenAIProviderGrammarMixin(BaseOpenAIInterpreter):
    _OPENAI_GRAMMAR_TOOL_NAME = "guidance_grammar"

    def _is_openai_official_client(self) -> bool:
        return "api.openai.com" in self._client_base_url()

    def _is_fireworks_client(self) -> bool:
        return "fireworks.ai" in self._client_base_url()

    def regex(self, node: RegexNode, **kwargs) -> Iterator[OutputAttr]:
        if node.regex is None:
            return self._run(**kwargs)

        if self._is_openrouter_client() or self._is_openai_official_client() or self._is_fireworks_client():
            return self.grammar(node, **kwargs)

        return super().regex(node, **kwargs)

    def grammar(self, node: GrammarNode, **kwargs) -> Iterator[OutputAttr]:
        if self._is_openrouter_client():
            return super().grammar(node, **kwargs)
        if self._is_openai_official_client():
            return self._grammar_via_openai_responses(node=node, kwargs=kwargs)
        if self._is_fireworks_client():
            return self._grammar_via_fireworks(node=node, kwargs=kwargs)
        return super().grammar(node, **kwargs)

    def _ensure_generation_context(self) -> None:
        if self.state.active_role is None:
            raise ValueError("OpenAI models require chat blocks (e.g. use `with assistant(): ...`)")
        if self.state.active_role != "assistant":
            raise ValueError(
                "OpenAI models can only generate as the assistant (i.e. inside of `with assistant(): ...`)"
            )
        if self.state.content:
            raise ValueError(
                f"OpenAI models do not support pre-filled assistant messages: got data {self.state.content}."
            )

    def _responses_input_messages(self) -> list[dict[str, Any]]:
        input_items: list[dict[str, Any]] = []
        for message in self.state.messages:
            if not isinstance(message, ContentMessage):
                raise ConstraintUnsupportedFeatureError(
                    "OpenAI Responses grammar path currently supports only role/content chat messages."
                )
            content_payload: list[dict[str, Any]] = []
            for content in message.content:
                if isinstance(content, TextContent):
                    content_payload.append({"type": "input_text", "text": content.text})
                elif isinstance(content, ImageUrlContent):
                    content_payload.append({"type": "input_image", "image_url": content.image_url.url})
                elif isinstance(content, AudioContent):
                    raise ConstraintUnsupportedFeatureError(
                        "OpenAI Responses grammar path does not support audio inputs yet."
                    )
                else:
                    raise ConstraintUnsupportedFeatureError(
                        f"Unsupported message content type for OpenAI Responses grammar path: {type(content).__name__}."
                    )
            input_items.append({"role": message.role, "content": content_payload})
        return input_items

    def _extract_custom_tool_output_text(self, response: Any, *, tool_name: str) -> str:  # noqa: ANN401
        output_items = getattr(response, "output", None)
        if not isinstance(output_items, list):
            raise ConstraintProviderRejectedError(
                f"OpenAI Responses grammar path for model '{self.model}' did not return an output list."
            )
        for item in output_items:
            if getattr(item, "type", None) != "custom_tool_call":
                continue
            if getattr(item, "name", None) != tool_name:
                continue
            input_text = getattr(item, "input", None)
            if isinstance(input_text, str):
                return input_text
        raise ConstraintProviderRejectedError(
            f"OpenAI Responses grammar path for model '{self.model}' returned no matching custom tool output."
        )

    def _grammar_via_openai_responses(self, *, node: GrammarNode, kwargs: dict[str, Any]) -> Iterator[OutputAttr]:
        self._ensure_generation_context()

        request_kwargs = dict(kwargs)
        sampling_params = request_kwargs.pop("sampling_params", None)
        if sampling_params:
            if "top_p" not in request_kwargs:
                request_kwargs["top_p"] = sampling_params.get("top_p", None)
            if sampling_params.get("top_k", None) is not None:
                raise ValueError("OpenAI Responses grammar path does not support top_k sampling.")
            if sampling_params.get("min_p", None) is not None:
                raise ValueError("OpenAI Responses grammar path does not support min_p sampling.")
            if sampling_params.get("repetition_penalty", None) is not None:
                raise ValueError("OpenAI Responses grammar path does not support repetition_penalty sampling.")

        max_output_tokens = request_kwargs.pop("max_output_tokens", None)
        if max_output_tokens is None:
            max_output_tokens = request_kwargs.pop("max_completion_tokens", None)
        if max_output_tokens is None:
            max_output_tokens = request_kwargs.pop("max_tokens", None)

        grammar_format = OpenAIResponsesGrammarBuilder().build(node)
        tool_name = self._OPENAI_GRAMMAR_TOOL_NAME
        input_messages = self._responses_input_messages()

        request_body: dict[str, Any] = {
            "model": self.model,
            "input": input_messages,
            "tools": [
                {
                    "type": "custom",
                    "name": tool_name,
                    "description": "Guidance constrained generation",
                    "format": grammar_format,
                }
            ],
            "tool_choice": {"type": "custom", "name": tool_name},
        }
        for key in ("temperature", "top_p"):
            value = request_kwargs.pop(key, None)
            if value is not None:
                request_body[key] = value
        if max_output_tokens is not None:
            request_body["max_output_tokens"] = max_output_tokens
        if "reasoning" in request_kwargs:
            request_body["reasoning"] = request_kwargs.pop("reasoning")
        elif self.reasoning_effort:
            request_body["reasoning"] = {"effort": self.reasoning_effort}

        # Preserve explicit passthroughs where the SDK supports them.
        for key in ("metadata", "user", "service_tier"):
            value = request_kwargs.pop(key, None)
            if value is not None:
                request_body[key] = value

        started = time.time()
        try:
            response = self.client.responses_create(**request_body)
        except Exception as exc:  # noqa: BLE001
            if looks_like_provider_rejection_error(str(exc)):
                raise ConstraintProviderRejectedError(
                    f"OpenAI Responses grammar path for model '{self.model}' rejected constrained generation."
                ) from exc
            raise

        usage_payload = getattr(response, "usage", None)
        usage = TokenUsage(round_trips=1)
        if usage_payload is not None:
            usage.input_tokens += int(getattr(usage_payload, "input_tokens", 0) or 0)
            usage.forward_passes += int(getattr(usage_payload, "output_tokens", 0) or 0)
            usage.cached_input_tokens += int(
                getattr(getattr(usage_payload, "input_tokens_details", None), "cached_tokens", 0) or 0
            )
        usage.total_latency_ms += (time.time() - started) * 1000
        usage.ttft_ms = usage.total_latency_ms
        self.state.add_usage(usage)

        generated_text = self._extract_custom_tool_output_text(response, tool_name=tool_name)
        if generated_text:
            self.state.apply_text(generated_text)
            yield TextOutput(value=generated_text, is_generated=True)

        yield from apply_local_constraint_validation(
            node=node,
            generated_text=generated_text,
            state=self.state,
            model=self.model,
            provider="OpenAI",
        )

    def _grammar_via_fireworks(self, *, node: GrammarNode, kwargs: dict[str, Any]) -> Iterator[OutputAttr]:
        grammar = FireworksGBNFBuilder().build(node)
        generated_text = ""

        try:
            for attr in self._run(
                response_format={
                    "type": "grammar",
                    "grammar": grammar,
                },
                **kwargs,
            ):
                if isinstance(attr, (TextOutput, TokenOutput)):
                    generated_text += attr.value
                yield attr
        except Exception as exc:  # noqa: BLE001
            if looks_like_provider_rejection_error(str(exc)):
                raise ConstraintProviderRejectedError(
                    f"Fireworks grammar path for model '{self.model}' rejected constrained generation."
                ) from exc
            raise

        yield from apply_local_constraint_validation(
            node=node,
            generated_text=generated_text,
            state=self.state,
            model=self.model,
            provider="Fireworks",
        )
