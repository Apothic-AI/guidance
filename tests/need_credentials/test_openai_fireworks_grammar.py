import os

import pytest

from guidance import assistant, gen, system, user
from guidance.models import OpenAI

from ..utils import env_or_skip, slowdown


def _availability_skip(exc: Exception) -> None:
    message = str(exc).lower()
    if any(
        marker in message
        for marker in (
            "rate limit",
            "rate-limit",
            "429",
            "temporarily",
            "timeout",
            "overloaded",
            "connection",
        )
    ):
        pytest.skip(f"Provider/model availability issue: {exc}")


@pytest.fixture(scope="function")
def openai_native_grammar_model():
    slowdown()
    api_key = env_or_skip("OPENAI_API_KEY")
    model_name = env_or_skip("OPENAI_GRAMMAR_MODEL")
    return OpenAI(model_name, api_key=api_key)


@pytest.fixture(scope="function")
def fireworks_grammar_model():
    slowdown()
    api_key = env_or_skip("FIREWORKS_API_KEY")
    model_name = env_or_skip("FIREWORKS_GRAMMAR_MODEL")
    base_url = os.getenv("FIREWORKS_BASE_URL", "https://api.fireworks.ai/inference/v1")
    return OpenAI(model_name, api_key=api_key, base_url=base_url)


def test_openai_native_grammar_regex_success(openai_native_grammar_model):
    lm = openai_native_grammar_model
    with system():
        lm += "You are concise."
    with user():
        lm += "Reply with the word MAYBE only."
    with assistant():
        try:
            lm += gen(name="answer", regex="YES|NO", max_tokens=8)
        except Exception as exc:  # noqa: BLE001
            _availability_skip(exc)
            raise
    assert lm["answer"].strip() in {"YES", "NO"}


def test_fireworks_native_grammar_regex_success(fireworks_grammar_model):
    lm = fireworks_grammar_model
    with system():
        lm += "You are concise."
    with user():
        lm += "Reply with the word MAYBE only."
    with assistant():
        try:
            lm += gen(name="answer", regex="YES|NO", max_tokens=8)
        except Exception as exc:  # noqa: BLE001
            _availability_skip(exc)
            raise
    assert lm["answer"].strip() in {"YES", "NO"}
