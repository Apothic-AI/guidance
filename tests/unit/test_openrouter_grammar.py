from typing import Any, Iterator

import pytest

from guidance._ast import RegexNode
from guidance._grammar import select
from guidance.models import _openai_base, _openrouter
from guidance.trace import TextOutput, Token, TokenOutput


class _DummyClientWrapper(_openai_base.BaseOpenAIClientWrapper):
    def __init__(self):
        self.base_url = "https://openrouter.ai/api/v1"
        self.api_key = "test-key"

    def streaming_chat_completions(  # noqa: ANN201
        self,
        model: str,
        messages: list[dict[str, Any]],
        logprobs: bool,
        **kwargs,
    ) -> Iterator[Any]:
        raise NotImplementedError


def _interpreter() -> _openrouter.OpenRouterInterpreter:
    interpreter = _openrouter.OpenRouterInterpreter(
        model="openai/gpt-4o-mini",
        client=_DummyClientWrapper(),
        reasoning_effort=None,
    )
    interpreter.state.active_role = "assistant"
    return interpreter


def test_openrouter_regex_none_uses_unconstrained_run(monkeypatch):
    interpreter = _interpreter()
    captured: dict[str, Any] = {}

    def fake_run(**kwargs):  # noqa: ANN001
        captured.update(kwargs)
        yield TextOutput(value="hello", is_generated=True)

    monkeypatch.setattr(interpreter, "_run", fake_run)
    outputs = list(interpreter.regex(RegexNode(None)))

    assert len(outputs) == 1
    assert outputs[0].value == "hello"
    assert "response_format" not in captured


def test_openrouter_grammar_sends_response_format(monkeypatch):
    interpreter = _interpreter()
    monkeypatch.setattr(interpreter, "_openrouter_supports_grammar_response_format", lambda request_kwargs: True)
    seen: dict[str, Any] = {}

    def fake_run(**kwargs):  # noqa: ANN001
        seen.update(kwargs)
        yield TextOutput(value="YES", is_generated=True)

    monkeypatch.setattr(interpreter, "_run", fake_run)
    outputs = list(interpreter.regex(RegexNode("YES|NO")))

    assert len(outputs) == 1
    assert outputs[0].value == "YES"
    assert seen["response_format"]["type"] == "grammar"
    assert "YES|NO" in seen["response_format"]["grammar"]


def test_openrouter_grammar_support_gate(monkeypatch):
    interpreter = _interpreter()
    monkeypatch.setattr(interpreter, "_openrouter_supports_grammar_response_format", lambda request_kwargs: False)

    with pytest.raises(ValueError, match="does not support grammar response formats"):
        list(interpreter.regex(RegexNode("YES|NO")))


def test_openrouter_grammar_wraps_provider_rejection(monkeypatch):
    interpreter = _interpreter()
    monkeypatch.setattr(interpreter, "_openrouter_supports_grammar_response_format", lambda request_kwargs: True)

    def fake_run(**kwargs):  # noqa: ANN001
        raise RuntimeError("Provider returned error: unsupported grammar")
        yield  # pragma: no cover

    monkeypatch.setattr(interpreter, "_run", fake_run)
    with pytest.raises(ValueError, match="rejected grammar-constrained generation"):
        list(interpreter.regex(RegexNode("YES|NO")))


def test_openrouter_grammar_rejects_output_that_fails_local_validation(monkeypatch):
    interpreter = _interpreter()
    monkeypatch.setattr(interpreter, "_openrouter_supports_grammar_response_format", lambda request_kwargs: True)

    def fake_run(**kwargs):  # noqa: ANN001
        yield TextOutput(value="MAYBE", is_generated=True)

    monkeypatch.setattr(interpreter, "_run", fake_run)
    with pytest.raises(ValueError, match="failed local grammar validation"):
        list(interpreter.regex(RegexNode("YES|NO")))


def test_openrouter_grammar_validates_token_output_stream(monkeypatch):
    interpreter = _interpreter()
    monkeypatch.setattr(interpreter, "_openrouter_supports_grammar_response_format", lambda request_kwargs: True)

    def fake_run(**kwargs):  # noqa: ANN001
        for piece in ("Y", "E", "S"):
            yield TokenOutput(
                value=piece,
                is_generated=True,
                token=Token(token=piece, bytes=b"", prob=1.0),
            )

    monkeypatch.setattr(interpreter, "_run", fake_run)
    outputs = list(interpreter.regex(RegexNode("YES|NO")))

    assert len(outputs) == 3
    assert "".join(output.value for output in outputs) == "YES"


def test_openrouter_grammar_applies_captures_from_match(monkeypatch):
    interpreter = _interpreter()
    monkeypatch.setattr(interpreter, "_openrouter_supports_grammar_response_format", lambda request_kwargs: True)
    node = select(["YES", "NO"], name="choice")

    def fake_run(**kwargs):  # noqa: ANN001
        yield TextOutput(value="YES", is_generated=True)

    monkeypatch.setattr(interpreter, "_run", fake_run)
    outputs = list(interpreter.run(node))

    assert any(isinstance(output, TextOutput) and output.value == "YES" for output in outputs)
    assert interpreter.state.captures["choice"]["value"] == "YES"


def test_openrouter_grammar_uses_gbnf_for_fireworks_provider(monkeypatch):
    interpreter = _interpreter()
    monkeypatch.setattr(interpreter, "_openrouter_supports_grammar_response_format", lambda request_kwargs: True)
    seen: dict[str, Any] = {}

    def fake_run(**kwargs):  # noqa: ANN001
        seen.update(kwargs)
        yield TextOutput(value="YES", is_generated=True)

    monkeypatch.setattr(interpreter, "_run", fake_run)
    _ = list(
        interpreter.regex(
            RegexNode("YES|NO"),
            extra_body={"provider": {"order": ["Fireworks"], "require_parameters": True}},
        )
    )
    assert seen["response_format"]["type"] == "grammar"
    grammar = seen["response_format"]["grammar"]
    assert "root" in grammar
    assert "%llguidance" not in grammar
