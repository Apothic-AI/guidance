import math
from types import SimpleNamespace
from typing import Any, Iterator

import pytest

from guidance._ast import LiteralNode, RegexNode, RuleNode
from guidance.models import _openai_base, _openrouter
from guidance.models._streaming_utils import (
    CaptureLogProbAccumulator,
    StreamingRegexStopMatcher,
    extract_chunk_logprob_tokens,
)
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


def _interpreter() -> _openrouter.OpenRouterRuleMixin:
    interpreter = _openrouter.OpenRouterRuleMixin(
        model="openai/gpt-4o-mini",
        client=_DummyClientWrapper(),
        reasoning_effort=None,
    )
    interpreter.state.active_role = "assistant"
    return interpreter


def _rule(
    *,
    capture: str | None = None,
    list_append: bool = False,
    stop: RegexNode | LiteralNode | None = None,
    stop_capture: str | None = None,
    suffix: LiteralNode | None = None,
) -> RuleNode:
    return RuleNode(
        name="gen",
        value=RegexNode(regex=None),
        capture=capture,
        list_append=list_append,
        stop=stop,
        stop_capture=stop_capture,
        suffix=suffix,
    )


def test_extract_chunk_logprob_tokens_handles_mixed_shapes():
    choice = SimpleNamespace(
        logprobs=SimpleNamespace(
            content=[
                SimpleNamespace(token="hello", logprob=-0.2, bytes=[104, 105], top_logprobs=None),
                {"token": " world", "logprob": "-1.5", "bytes": [32, 119], "top_logprobs": [{"token": " there"}]},
            ]
        )
    )

    tokens = extract_chunk_logprob_tokens(choice)
    assert len(tokens) == 2
    assert tokens[0].token == "hello"
    assert tokens[0].token_bytes == b"hi"
    assert tokens[0].top_logprobs == ()
    assert tokens[1].token == " world"
    assert tokens[1].logprob == pytest.approx(-1.5)
    assert len(tokens[1].top_logprobs) == 1


def test_capture_logprob_accumulator_requires_exact_token_alignment():
    acc = CaptureLogProbAccumulator()
    acc.add("hello ", -0.3)
    acc.add("world", -0.2)

    assert acc.logprob_for_text("hello world") == pytest.approx(-0.5)
    assert acc.logprob_for_text("hello worl") is None
    assert acc.logprob_for_text("hello world!") is None


def test_streaming_regex_stop_matcher_spanning_chunks():
    matcher = StreamingRegexStopMatcher("STOP")
    assert matcher.feed("hello ST").emit_text == "hello"

    update = matcher.feed("OP world")
    assert update.matched is True
    assert update.emit_text == " "
    assert update.stop_text == "STOP"
    assert matcher.emitted_text == "hello "


def test_streaming_regex_stop_matcher_earliest_end_for_ties():
    matcher = StreamingRegexStopMatcher("ab|a")
    update = matcher.feed("cabd")
    assert update.matched is True
    assert update.emit_text == "c"
    assert update.stop_text == "a"


def test_streaming_regex_stop_matcher_no_match_emits_on_finish():
    matcher = StreamingRegexStopMatcher("a+b+")
    assert matcher.feed("xyz").emit_text == ""
    assert matcher.finish().emit_text == "xyz"


def test_openrouter_client_wrapper_omits_unsupported_logprob_fields():
    captured: dict[str, Any] = {}

    class _Context:
        def __enter__(self):
            return iter(())

        def __exit__(self, exc_type, exc, tb):
            return False

    class _FakeChat:
        def send(self, **kwargs):
            captured.update(kwargs)
            return _Context()

    class _FakeClient:
        def __init__(self):
            self.chat = _FakeChat()

    wrapper = _openrouter.OpenRouterClientWrapper(_FakeClient())
    wrapper.streaming_chat_completions(
        model="openai/gpt-4o-mini",
        messages=[],
        logprobs=False,
        top_logprobs=5,
    )

    assert "logprobs" not in captured
    assert "top_logprobs" not in captured


def test_openrouter_rule_regex_stop_capture_in_one_chunk(monkeypatch):
    interpreter = _interpreter()

    def fake_run(node, **kwargs):  # noqa: ANN001
        assert "stop" not in kwargs
        text = "hello STOP world"
        interpreter.state.apply_text(text)
        yield TextOutput(value=text, is_generated=True)

    monkeypatch.setattr(interpreter, "run", fake_run)

    outputs = list(
        interpreter.rule(
            _rule(
                capture="captured",
                stop=RegexNode("STOP"),
                stop_capture="stopped",
            )
        )
    )

    text = "".join(chunk.value for chunk in outputs if isinstance(chunk, TextOutput))
    assert text == "hello "
    assert interpreter.state.captures["captured"]["value"] == "hello "
    assert interpreter.state.captures["stopped"]["value"] == "STOP"
    assert interpreter.state.content[-1].text == "hello "


def test_openrouter_rule_regex_stop_spanning_chunks(monkeypatch):
    interpreter = _interpreter()

    def fake_run(node, **kwargs):  # noqa: ANN001
        parts = ["hello ST", "OP world"]
        for part in parts:
            interpreter.state.apply_text(part)
            yield TextOutput(value=part, is_generated=True)

    monkeypatch.setattr(interpreter, "run", fake_run)
    outputs = list(interpreter.rule(_rule(stop=RegexNode("STOP"))))

    text = "".join(chunk.value for chunk in outputs if isinstance(chunk, TextOutput))
    assert text == "hello "
    assert interpreter.state.content[-1].text == "hello "


def test_openrouter_rule_regex_stop_no_match(monkeypatch):
    interpreter = _interpreter()

    def fake_run(node, **kwargs):  # noqa: ANN001
        text = "hello world"
        interpreter.state.apply_text(text)
        yield TextOutput(value=text, is_generated=True)

    monkeypatch.setattr(interpreter, "run", fake_run)
    outputs = list(interpreter.rule(_rule(capture="captured", stop=RegexNode("STOP"), stop_capture="stopped")))

    text = "".join(chunk.value for chunk in outputs if isinstance(chunk, TextOutput))
    assert text == "hello world"
    assert interpreter.state.captures["captured"]["value"] == "hello world"
    assert "stopped" not in interpreter.state.captures


def test_openrouter_rule_capture_logprob_aggregation(monkeypatch):
    interpreter = _interpreter()

    def fake_run(node, **kwargs):  # noqa: ANN001
        for text, logprob in (("hello ", -0.2), ("world", -0.4)):
            interpreter.state.apply_text(text)
            yield TokenOutput(
                value=text,
                is_generated=True,
                token=Token(token=text, bytes=b"", prob=math.exp(logprob)),
            )

    monkeypatch.setattr(interpreter, "run", fake_run)
    list(interpreter.rule(_rule(capture="captured")))

    assert interpreter.state.captures["captured"]["value"] == "hello world"
    assert interpreter.state.captures["captured"]["log_prob"] == pytest.approx(-0.6)


def test_openrouter_rule_list_append_capture(monkeypatch):
    interpreter = _interpreter()
    values = ["one", "two"]

    def fake_run(node, **kwargs):  # noqa: ANN001
        value = values.pop(0)
        interpreter.state.apply_text(value)
        yield TextOutput(value=value, is_generated=True)

    monkeypatch.setattr(interpreter, "run", fake_run)
    node = _rule(capture="items", list_append=True)

    list(interpreter.rule(node))
    list(interpreter.rule(node))

    assert interpreter.state.captures["items"][0]["value"] == "one"
    assert interpreter.state.captures["items"][1]["value"] == "two"


def test_openrouter_rule_literal_stop_unchanged(monkeypatch):
    interpreter = _interpreter()

    def fake_run(node, **kwargs):  # noqa: ANN001
        assert kwargs["stop"] == "END"
        text = "value"
        interpreter.state.apply_text(text)
        yield TextOutput(value=text, is_generated=True)

    monkeypatch.setattr(interpreter, "run", fake_run)
    outputs = list(interpreter.rule(_rule(stop=LiteralNode("END"))))

    text = "".join(chunk.value for chunk in outputs if isinstance(chunk, TextOutput))
    assert text == "value"


def test_openrouter_rule_rejects_suffix_and_non_regex_stop_capture():
    interpreter = _interpreter()
    with pytest.raises(ValueError, match="Suffix not yet supported"):
        list(interpreter.rule(_rule(suffix=LiteralNode("suffix"))))
    with pytest.raises(ValueError, match="Save stop text is only supported with stop_regex"):
        list(interpreter.rule(_rule(stop=LiteralNode("END"), stop_capture="stopped")))


def test_openrouter_rule_raises_for_invalid_stop_regex():
    interpreter = _interpreter()
    with pytest.raises(ValueError, match="Invalid stop_regex pattern"):
        list(interpreter.rule(_rule(stop=RegexNode("["))))
