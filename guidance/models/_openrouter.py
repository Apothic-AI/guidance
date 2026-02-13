from __future__ import annotations

from typing import Any, Iterator, cast

from pydantic import TypeAdapter

from .._ast import LiteralNode, RegexNode, RuleNode
from .._schema import SamplingParams
from .._tools import Tool
from ..trace import OutputAttr, TextOutput
from ._base import Model
from ._openai_base import (
    BaseOpenAIClientWrapper,
    BaseOpenAIInterpreter,
    Message,
    OpenAIAudioMixin,
    OpenAIImageMixin,
    OpenAIJSONMixin,
    OpenAIRegexMixin,
)
from ._openrouter_capabilities import _extract_openrouter_model_modalities, resolve_openrouter_model_metadata


class OpenRouterClientWrapper(BaseOpenAIClientWrapper):
    def __init__(self, client: "openrouter.OpenRouter", *, server_url: str | None = None, api_key: str | None = None):
        self.client = client
        self.base_url = server_url or "https://openrouter.ai/api/v1"
        self.api_key = api_key or ""

    def streaming_chat_completions(
        self,
        model: str,
        messages: list[dict[str, Any]],
        logprobs: bool,
        **kwargs,
    ):
        return self.client.chat.send(
            model=model,
            messages=messages,
            logprobs=logprobs,
            stream=True,
            stream_options={"include_usage": True},
            **kwargs,
        )


class OpenRouterRuleMixin(BaseOpenAIInterpreter):
    def rule(self, node: RuleNode, **kwargs) -> Iterator[OutputAttr]:
        if node.suffix:
            raise ValueError("Suffix not yet supported for OpenRouter")
        if node.stop_capture:
            raise ValueError("Save stop text not yet supported for OpenRouter")

        kwargs = kwargs.copy()
        if node.temperature:
            kwargs["temperature"] = node.temperature
        if node.max_tokens:
            kwargs["max_tokens"] = node.max_tokens
        if node.stop:
            if isinstance(node.stop, LiteralNode):
                kwargs["stop"] = node.stop.value
            elif isinstance(node.stop, RegexNode):
                raise ValueError("Regex stop conditions are not yet supported for OpenRouter")
            else:
                raise ValueError("Unsupported stop node type for OpenRouter")

        chunks = self.run(node.value, **kwargs)
        if node.capture:
            buffered_text = ""
            for chunk in chunks:
                if isinstance(chunk, TextOutput):
                    buffered_text += chunk.value
                yield chunk
            yield self.state.apply_capture(
                name=node.capture,
                value=buffered_text,
                log_prob=1,  # TODO
                is_append=node.list_append,
            )
        else:
            yield from chunks


class OpenRouterInterpreter(OpenRouterRuleMixin, OpenAIJSONMixin, OpenAIRegexMixin, BaseOpenAIInterpreter):
    def _is_openrouter_client(self) -> bool:
        return True

    def _run(self, tools: dict[str, Tool] | None = None, **kwargs) -> Iterator[OutputAttr]:
        if self.state.active_role is None:
            raise ValueError("OpenRouter models require chat blocks (e.g. use `with assistant(): ...`)")
        if self.state.active_role != "assistant":
            raise ValueError(
                "OpenRouter models can only generate as the assistant (i.e. inside of `with assistant(): ...`)"
            )

        messages = list(self.state.messages)
        active_message = self.state.get_active_message()
        if active_message is not None:
            messages.append(active_message)

        request_kwargs = dict(kwargs)
        sampling_params = request_kwargs.pop("sampling_params", None)
        if sampling_params:
            if "top_p" not in request_kwargs:
                request_kwargs["top_p"] = sampling_params.get("top_p", None)

            top_k = sampling_params.get("top_k", None)
            if top_k is not None:
                request_kwargs["top_k"] = top_k

            min_p = sampling_params.get("min_p", None)
            if min_p is not None:
                request_kwargs["min_p"] = min_p

            repetition_penalty = sampling_params.get("repetition_penalty", None)
            if repetition_penalty is not None:
                request_kwargs["repetition_penalty"] = repetition_penalty

        if "reasoning_effort" not in request_kwargs and self.reasoning_effort is not None:
            request_kwargs["reasoning_effort"] = self.reasoning_effort

        request_kwargs = self._apply_openrouter_request_overrides(request_kwargs)
        if tools and not self._openrouter_supports_tools(request_kwargs):
            raise ValueError(f"OpenRouter model '{self.model}' does not support tool calls.")

        request_logprobs = self.logprobs
        top_logprobs = self.top_k if request_logprobs else None
        supports_logprobs, supports_top_logprobs = self._openrouter_logprobs_capability(request_kwargs)
        if not supports_logprobs:
            request_logprobs = False
            top_logprobs = None
        elif not supports_top_logprobs:
            top_logprobs = None

        with self.client.streaming_chat_completions(
            model=self.model,
            messages=cast(list[dict[str, Any]], TypeAdapter(list[Message]).dump_python(messages)),
            logprobs=request_logprobs,
            top_logprobs=top_logprobs,
            tools=[tool.with_name(name).to_openai_style() for name, tool in tools.items()] if tools else None,
            **request_kwargs,
        ) as chunks:
            yield from self._handle_stream(chunks, tools)


class OpenRouter(Model):
    def __init__(
        self,
        model: str,
        sampling_params: SamplingParams | None = None,
        echo: bool = True,
        *,
        api_key: str | None = None,
        reasoning_effort: str | None = None,
        http_referer: str | None = None,
        x_title: str | None = None,
        server_url: str | None = None,
        **kwargs,
    ):
        try:
            import openrouter
        except ImportError as ie:
            raise Exception(
                "Please install the openrouter package using `pip install openrouter` in order to use guidance.models.OpenRouter!"
            ) from ie

        client = openrouter.OpenRouter(
            api_key=api_key,
            http_referer=http_referer,
            x_title=x_title,
            server_url=server_url,
            **kwargs,
        )

        model_meta = resolve_openrouter_model_metadata(
            model=model,
            api_base=server_url or "https://openrouter.ai/api/v1",
            api_key=api_key or "",
        )
        input_modalities, output_modalities = _extract_openrouter_model_modalities(model_meta)
        has_audio = "audio" in input_modalities or "audio" in output_modalities
        has_image = "image" in input_modalities

        if not has_audio and not has_image and "audio-preview" in model:
            has_audio = True
        if not has_audio and not has_image and ("gpt-4o" in model or "o1" in model):
            has_image = True

        if has_audio and has_image:
            interpreter_cls = type(
                "OpenRouterAudioImageInterpreter",
                (OpenAIAudioMixin, OpenAIImageMixin, OpenRouterInterpreter),
                {},
            )
        elif has_audio:
            interpreter_cls = type("OpenRouterAudioInterpreter", (OpenAIAudioMixin, OpenRouterInterpreter), {})
        elif has_image:
            interpreter_cls = type("OpenRouterImageInterpreter", (OpenAIImageMixin, OpenRouterInterpreter), {})
        else:
            interpreter_cls = OpenRouterInterpreter

        super().__init__(
            interpreter=interpreter_cls(
                model,
                client=OpenRouterClientWrapper(client, server_url=server_url, api_key=api_key),
                reasoning_effort=reasoning_effort,
            ),
            sampling_params=SamplingParams() if sampling_params is None else sampling_params,
            echo=echo,
        )
