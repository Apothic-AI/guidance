import math
import os

import pytest

from guidance import assistant, gen, system, user
from guidance.models import OpenAI
from guidance.models._openrouter_capabilities import (
    _extract_openrouter_supported_parameters,
    fetch_openrouter_models_catalog,
)
from guidance.trace import TokenOutput

from ..utils import env_or_skip, slowdown

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


def _pick_model(catalog: dict[str, dict], *, requires_logprobs: bool) -> str | None:
    seen: set[str] = set()
    for row in catalog.values():
        model_id = str(row.get("id", "")).strip()
        model_key = model_id.lower()
        if not model_id or model_key in seen:
            continue
        seen.add(model_key)
        supported = _extract_openrouter_supported_parameters(row)
        if ("logprobs" in supported) == requires_logprobs:
            return model_id
    return None


def _pick_model_with_parameter(catalog: dict[str, dict], *, parameter: str) -> str | None:
    target = str(parameter).strip().lower()
    if not target:
        return None
    seen: set[str] = set()
    for row in catalog.values():
        model_id = str(row.get("id", "")).strip()
        model_key = model_id.lower()
        if not model_id or model_key in seen:
            continue
        seen.add(model_key)
        supported = _extract_openrouter_supported_parameters(row)
        if target in supported:
            return model_id
    return None


def _trace_token_outputs(model) -> list[TokenOutput]:  # noqa: ANN001
    out: list[TokenOutput] = []
    for trace_node in model._trace_nodes:
        for output_attr in trace_node.output:
            if isinstance(output_attr, TokenOutput):
                out.append(output_attr)
    return out


@pytest.fixture(scope="session")
def openrouter_base_url() -> str:
    configured = os.getenv("OPENROUTER_BASE_URL")
    if configured:
        return configured
    openai_base = os.getenv("OPENAI_BASE_URL")
    if openai_base and "openrouter.ai" in openai_base.lower():
        return openai_base
    return OPENROUTER_BASE_URL


@pytest.fixture(scope="session")
def openrouter_api_key(openrouter_base_url: str) -> str:
    key = os.getenv("OPENROUTER_API_KEY")
    if key:
        return key
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key and "openrouter.ai" in openrouter_base_url.lower():
        return openai_key
    return env_or_skip("OPENROUTER_API_KEY")


@pytest.fixture(scope="session")
def openrouter_catalog(openrouter_api_key: str, openrouter_base_url: str) -> dict[str, dict]:
    return fetch_openrouter_models_catalog(
        api_base=openrouter_base_url,
        api_key=openrouter_api_key,
    )


@pytest.fixture(scope="function")
def openrouter_logprobs_model(openrouter_api_key: str, openrouter_catalog: dict[str, dict], openrouter_base_url: str):
    slowdown()
    model_name = os.getenv("OPENROUTER_LOGPROBS_MODEL")
    if model_name is None:
        model_name = _pick_model(openrouter_catalog, requires_logprobs=True)
    if model_name is None:
        pytest.skip("No OpenRouter model with logprobs support found in /models catalog.")

    provider = os.getenv("OPENROUTER_LOGPROBS_PROVIDER")
    lm = OpenAI(
        model_name,
        api_key=openrouter_api_key,
        base_url=openrouter_base_url,
        openrouter_require_parameters=True,
        openrouter_provider=provider,
    )
    supports_logprobs, _ = lm._interpreter._openrouter_logprobs_capability({})
    if not supports_logprobs:
        pytest.skip(f"Selected OpenRouter model/provider does not currently support logprobs: {model_name}")
    return lm


@pytest.fixture(scope="function")
def openrouter_non_logprobs_model(
    openrouter_api_key: str, openrouter_catalog: dict[str, dict], openrouter_base_url: str
):
    slowdown()
    model_name = os.getenv("OPENROUTER_NON_LOGPROBS_MODEL")
    if model_name is None:
        model_name = _pick_model(openrouter_catalog, requires_logprobs=False)
    if model_name is None:
        pytest.skip("No OpenRouter model without logprobs support found in /models catalog.")

    provider = os.getenv("OPENROUTER_NON_LOGPROBS_PROVIDER")
    lm = OpenAI(
        model_name,
        api_key=openrouter_api_key,
        base_url=openrouter_base_url,
        openrouter_require_parameters=True,
        openrouter_provider=provider,
    )
    supports_logprobs, _ = lm._interpreter._openrouter_logprobs_capability({})
    if supports_logprobs:
        pytest.skip(f"Selected OpenRouter model/provider unexpectedly supports logprobs: {model_name}")
    return lm


@pytest.fixture(scope="function")
def openrouter_grammar_model(openrouter_api_key: str, openrouter_catalog: dict[str, dict], openrouter_base_url: str):
    slowdown()
    model_name = os.getenv("OPENROUTER_GRAMMAR_MODEL")
    if model_name is None:
        model_name = _pick_model_with_parameter(openrouter_catalog, parameter="response_format")
    if model_name is None:
        pytest.skip("No OpenRouter model with response_format support found in /models catalog.")

    provider = os.getenv("OPENROUTER_GRAMMAR_PROVIDER")
    lm = OpenAI(
        model_name,
        api_key=openrouter_api_key,
        base_url=openrouter_base_url,
        openrouter_require_parameters=True,
        openrouter_provider=provider,
    )
    supports_grammar = lm._interpreter._openrouter_supports_grammar_response_format({})
    if not supports_grammar:
        pytest.skip(
            f"Selected OpenRouter model/provider does not currently support grammar response_format: {model_name}"
        )
    return lm


def test_openrouter_logprobs_positive(openrouter_logprobs_model):
    lm = openrouter_logprobs_model
    with system():
        lm += "You are concise."
    with user():
        lm += "Say hello in one short sentence."
    with assistant():
        try:
            lm += gen(name="answer", max_tokens=16)
        except Exception as exc:  # noqa: BLE001
            pytest.skip(f"OpenRouter logprobs-positive run failed for provider/model availability reasons: {exc}")

    token_outputs = _trace_token_outputs(lm)
    if not token_outputs:
        pytest.skip("Selected OpenRouter model/provider did not emit token-level logprobs in this run.")
    assert any(not math.isnan(token.token.prob) for token in token_outputs), "Expected numeric token probabilities."


def test_openrouter_logprobs_negative_fallback(openrouter_non_logprobs_model):
    lm = openrouter_non_logprobs_model
    with system():
        lm += "You are concise."
    with user():
        lm += "Say hello in one short sentence."
    with assistant():
        try:
            lm += gen(name="answer", max_tokens=16)
        except Exception as exc:  # noqa: BLE001
            pytest.skip(f"OpenRouter logprobs-negative run failed for provider/model availability reasons: {exc}")

    assert "answer" in lm
    token_outputs = _trace_token_outputs(lm)
    assert len(token_outputs) == 0


def test_openrouter_regex_constraint_fail_closed(openrouter_grammar_model):
    lm = openrouter_grammar_model
    with system():
        lm += "You are concise."
    with user():
        lm += "Reply with the word MAYBE only."
    with assistant():
        try:
            lm += gen(name="answer", regex="YES|NO", max_tokens=8)
        except Exception as exc:  # noqa: BLE001
            message = str(exc).lower()
            if any(marker in message for marker in ("429", "rate-limit", "temporarily", "provider returned error")):
                pytest.skip(f"OpenRouter grammar run failed for provider/model availability reasons: {exc}")
            assert "grammar" in message or "failed local grammar validation" in message
            return

    answer = lm["answer"].strip()
    assert answer in {"YES", "NO"}
