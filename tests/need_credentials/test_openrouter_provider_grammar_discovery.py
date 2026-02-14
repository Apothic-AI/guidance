import json
import os
import subprocess
from pathlib import Path

import pytest

from ..utils import env_or_skip


@pytest.mark.skipif(
    os.getenv("OPENROUTER_ENABLE_GRAMMAR_PROBE_TEST") != "1",
    reason="Set OPENROUTER_ENABLE_GRAMMAR_PROBE_TEST=1 to run provider grammar discovery test.",
)
def test_openrouter_provider_grammar_discovery_script(tmp_path: Path):
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        env_or_skip("OPENROUTER_API_KEY")
    models = os.getenv("OPENROUTER_FEATURE_TEST_MODELS")
    if not models:
        env_or_skip("OPENROUTER_FEATURE_TEST_MODELS")

    markdown_path = tmp_path / "provider-capabilities.md"
    json_path = tmp_path / "provider-capabilities.json"
    command = [
        "python",
        "scripts/openrouter_provider_grammar_discovery.py",
        "--models",
        str(models),
        "--formats",
        "ll-lark",
        "--per-model-provider-limit",
        "1",
        "--output-markdown",
        str(markdown_path),
        "--output-json",
        str(json_path),
    ]
    completed = subprocess.run(command, check=False, capture_output=True, text=True)  # noqa: S603
    assert completed.returncode == 0, completed.stderr or completed.stdout

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload.get("schema_version") == 1
    assert isinstance(payload.get("models"), list) and len(payload["models"]) > 0
    assert isinstance(payload.get("providers"), dict)
    assert isinstance(payload.get("models_summary"), dict)
