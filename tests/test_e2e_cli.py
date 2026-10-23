import subprocess
import sys
import pytest

@pytest.mark.e2e
def test_cli_without_arguments_prints_and_exits_1():
    result = subprocess.run(
        [sys.executable, "main.py"],
        capture_output=True, text=True
    )

    assert result.returncode == 1
    assert "Usage:" in result.stderr
    assert result.stdout == ""