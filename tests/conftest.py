import pytest

@pytest.fixture(autouse=True)
def isolate_log_file(tmp_path, monkeypatch):
    monkeypatch.setenv("LOG_FILE", str(tmp_path / "test.log"))