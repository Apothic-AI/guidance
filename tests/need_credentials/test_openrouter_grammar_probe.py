import json
import os
import subprocess
from pathlib import Path

import pytest

from ..utils import env_or_skip


@pytest.mark.skipif(
    os.getenv("OPENROUTER_ENABLE_GRAMMAR_PROBE_TEST") != "1",
    reason="Set OPENROUTER_ENABLE_GRAMMAR_PROBE_TEST=1 to run probe matrix test.",
)
def test_openrouter_probe_matrix_script(tmp_path: Path):
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        env_or_skip("OPENROUTER_API_KEY")
    model = os.getenv("OPENROUTER_GRAMMAR_PROBE_MODEL") or os.getenv("OPENROUTER_GRAMMAR_MODEL")
    if not model:
        env_or_skip("OPENROUTER_GRAMMAR_PROBE_MODEL")

    markdown_path = tmp_path / "matrix.md"
    json_path = tmp_path / "matrix.json"
    command = [
        "python",
        "scripts/openrouter_grammar_probe.py",
        "--model",
        str(model),
        "--limit",
        "1",
        "--output-markdown",
        str(markdown_path),
        "--output-json",
        str(json_path),
    ]
    completed = subprocess.run(command, check=False, capture_output=True, text=True)  # noqa: S603
    assert completed.returncode == 0, completed.stderr or completed.stdout
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    results = payload.get("results")
    assert isinstance(results, list) and len(results) > 0
    allowed_outcomes = {"reject", "accepts+obeys", "accepts+ignores"}
    assert all(result.get("outcome") in allowed_outcomes for result in results if isinstance(result, dict))
