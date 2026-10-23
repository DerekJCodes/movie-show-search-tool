import subprocess
import sys
import pytest
import os
import re

def run_cli(*args):
    return subprocess.run(
        [sys.executable, "main.py", *args],
        capture_output=True, text=True, encoding="utf-8",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"}
    )


@pytest.mark.e2e
def test_cli_without_arguments_prints_and_exits_1():
    result = subprocess.run(
        [sys.executable, "main.py"],
        capture_output=True, text=True
    )

    assert result.returncode == 1
    assert "Usage:" in result.stderr
    assert result.stdout == ""

@pytest.mark.e2e
def test_search_then_open_details():
    search = run_cli("search", "spider-man")
    if "Couldn't reach TMDB" in search.stderr:
        pytest.skip("TMDB unreachable, cannot run this E2E test")

    assert search.returncode == 0
    match = re.search(r"\[Movie\] Spider-Man \(2002\).*id: (\d+)", search.stdout)
    assert match is not None
    movie_id = match.group(1)

    details = run_cli("details", "movie", movie_id)

    assert details.returncode == 0
    assert "Spider-Man (2002)" in details.stdout