from types import SimpleNamespace
from typing import Any, Iterator

import pytest

from guidance._ast import LiteralNode, RegexNode, RuleNode, SelectNode
from guidance._grammar import select
from guidance.models import _openai_base
from guidance.models._grammar_support import (
    ConstraintUnsupportedFeatureError,
    FireworksGBNFBuilder,
    OpenAIResponsesGrammarBuilder,
)
from guidance.models._openai_base import BaseOpenAIInterpreter, OpenAIRegexMixin
from guidance.models._openai_provider_grammar import OpenAIProviderGrammarMixin
from guidance.models._openrouter_grammar import OpenRouterGrammarMixin
from guidance.trace import TextOutput


class _DummyClientWrapper(_openai_base.BaseOpenAIClientWrapper):
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.api_key = "test-key"
        self.responses_kwargs: dict[str, Any] | None = None

    def streaming_chat_completions(  # noqa: ANN201
        self,
        model: str,
        messages: list[dict[str, Any]],
        logprobs: bool,
        **kwargs,
    ) -> Iterator[Any]:
        raise NotImplementedError

    def responses_create(self, **kwargs) -> Any:  # noqa: ANN401
        self.responses_kwargs = dict(kwargs)
        return SimpleNamespace(
            output=[
                SimpleNamespace(
                    type="custom_tool_call",
                    name="guidance_grammar",
                    input="YES",
                )
            ],
            usage=SimpleNamespace(
                input_tokens=4,
                output_tokens=1,
                input_tokens_details=SimpleNamespace(cached_tokens=0),
            ),
        )


class _Interpreter(
    OpenAIProviderGrammarMixin,
    OpenRouterGrammarMixin,
    OpenAIRegexMixin,
    BaseOpenAIInterpreter,
):
    pass


def _interpreter(base_url: str) -> tuple[_Interpreter, _DummyClientWrapper]:
    client = _DummyClientWrapper(base_url)
    interpreter = _Interpreter(
        model="test-model",
        client=client,
        reasoning_effort=None,
    )
    interpreter.state.active_role = "assistant"
    return interpreter, client


def test_openai_responses_regex_path_builds_custom_tool_grammar_request():
    interpreter, client = _interpreter("https://api.openai.com/v1")
    outputs = list(interpreter.regex(RegexNode("YES|NO"), max_completion_tokens=7))
    assert len(outputs) == 1
    assert isinstance(outputs[0], TextOutput)
    assert outputs[0].value == "YES"

    assert client.responses_kwargs is not None
    assert client.responses_kwargs["max_output_tokens"] == 7
    assert client.responses_kwargs["tool_choice"]["type"] == "custom"
    tool = client.responses_kwargs["tools"][0]
    assert tool["type"] == "custom"
    assert tool["format"]["type"] == "grammar"
    assert tool["format"]["syntax"] == "regex"
    assert tool["format"]["definition"] == "YES|NO"


def test_openai_responses_grammar_path_applies_captures():
    interpreter, _ = _interpreter("https://api.openai.com/v1")
    node = select(["YES", "NO"], name="choice")
    _ = list(interpreter.run(node))
    assert interpreter.state.captures["choice"]["value"] == "YES"


def test_openai_responses_grammar_provider_rejection(monkeypatch):
    interpreter, client = _interpreter("https://api.openai.com/v1")

    def reject(**kwargs):  # noqa: ANN001
        raise RuntimeError("unsupported grammar format")

    monkeypatch.setattr(client, "responses_create", reject)
    with pytest.raises(ValueError, match="rejected constrained generation"):
        list(interpreter.regex(RegexNode("YES|NO")))


def test_fireworks_grammar_path_sets_response_format(monkeypatch):
    interpreter, _ = _interpreter("https://api.fireworks.ai/inference/v1")
    seen: dict[str, Any] = {}

    def fake_run(**kwargs):  # noqa: ANN001
        seen.update(kwargs)
        yield TextOutput(value="YES", is_generated=True)

    monkeypatch.setattr(interpreter, "_run", fake_run)
    outputs = list(interpreter.regex(RegexNode("YES|NO")))
    assert len(outputs) == 1
    assert outputs[0].value == "YES"
    assert seen["response_format"]["type"] == "grammar"
    assert "root" in seen["response_format"]["grammar"]


def test_fireworks_grammar_path_fails_closed_on_local_validation(monkeypatch):
    interpreter, _ = _interpreter("https://api.fireworks.ai/inference/v1")

    def fake_run(**kwargs):  # noqa: ANN001
        yield TextOutput(value="MAYBE", is_generated=True)

    monkeypatch.setattr(interpreter, "_run", fake_run)
    with pytest.raises(ValueError, match="failed local grammar validation"):
        list(interpreter.regex(RegexNode("YES|NO")))


def test_fireworks_streams_reasoning_content_as_generated_text():
    interpreter, _ = _interpreter("https://api.fireworks.ai/inference/v1")

    def _chunk(*, role: str | None = None, reasoning_content: str | None = None, finish: str | None = None):
        delta = SimpleNamespace(
            content=None,
            reasoning_content=reasoning_content,
            role=role,
            function_call=None,
            tool_calls=None,
            refusal=None,
            audio=None,
        )
        choice = SimpleNamespace(delta=delta, finish_reason=finish, logprobs=None)
        return SimpleNamespace(choices=[choice], usage=None)

    chunks = iter(
        [
            _chunk(role="assistant"),
            _chunk(reasoning_content="Y"),
            _chunk(reasoning_content="E"),
            _chunk(reasoning_content="S"),
            _chunk(finish="stop"),
        ]
    )
    outputs = list(interpreter._handle_stream(chunks, tools=None))
    emitted = "".join(output.value for output in outputs if isinstance(output, TextOutput))

    assert emitted == "YES"
    assert interpreter.state.content
    assert interpreter.state.content[-1].text == "YES"


def test_non_openai_endpoints_keep_existing_regex_behavior():
    interpreter, _ = _interpreter("https://example.invalid/v1")
    with pytest.raises(ValueError, match="Regex not yet supported for OpenAI"):
        list(interpreter.regex(RegexNode("YES|NO")))


def test_openai_builder_select_literals_uses_regex():
    grammar = OpenAIResponsesGrammarBuilder().build(SelectNode((LiteralNode("YES"), LiteralNode("NO"))))
    assert grammar["syntax"] == "regex"
    assert "YES" in grammar["definition"]
    assert "NO" in grammar["definition"]


def test_openai_builder_rejects_rule_attrs():
    builder = OpenAIResponsesGrammarBuilder()
    node = RuleNode(name="start", value=RegexNode("[A-Z]+"), max_tokens=3)
    with pytest.raises(ConstraintUnsupportedFeatureError, match="RuleNode attrs"):
        builder.build(node)


def test_fireworks_gbnf_builder_regex_subset():
    grammar = FireworksGBNFBuilder().build(RegexNode("YES|NO"))
    assert "root" in grammar
    assert "|" in grammar


def test_fireworks_gbnf_builder_rejects_unsupported_regex_constructs():
    with pytest.raises(ConstraintUnsupportedFeatureError):
        FireworksGBNFBuilder().build(RegexNode("(?=A)A"))
