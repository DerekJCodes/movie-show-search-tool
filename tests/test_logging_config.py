import logging
import pytest
from logging_config import configure_logging

@pytest.fixture(autouse=True)
def clean_root_logger():
    root = logging.getLogger()
    handlers_before = root.handlers[:]
    level_before = root.level
    yield
    for h in root.handlers[:]:
        if h not in handlers_before:
            root.removeHandler(h)
            h.close()
    root.setLevel(level_before)
    logging.getLogger("urllib3").setLevel(logging.NOTSET)

def test_configure_logging_writes_to_file_not_terminal(tmp_path, capsys):
    log_file = tmp_path / "test.log"
    configure_logging(log_file=str(log_file), level="INFO")

    logging.getLogger("services.test").info("hello")

    text = log_file.read_text()
    assert "INFO" in text
    assert "services.test" in text
    assert "hello" in text
    assert capsys.readouterr().out == ""

def test_log_level_comes_from_environment(tmp_path, monkeypatch):
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    log_file = tmp_path / "test.log"
    configure_logging(log_file=str(log_file))

    logging.getLogger("services.test").debug("detail")

    assert "detail" in log_file.read_text()

def test_default_level_hides_debug(tmp_path, monkeypatch):
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    log_file = tmp_path / "test.log"
    configure_logging(log_file=str(log_file))

    logging.getLogger("services.test").debug("detail")

    assert "detail" not in log_file.read_text()

def test_log_file_comes_from_environment(tmp_path, monkeypatch):
    log_file = tmp_path / "from_env.log"
    monkeypatch.setenv("LOG_FILE", str(log_file))
    configure_logging()

    logging.getLogger("services.test").info("hello")

    assert "hello" in log_file.read_text()