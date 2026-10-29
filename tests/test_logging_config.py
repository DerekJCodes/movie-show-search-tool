import logging
import pytest
from logging_config import configure_logging

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
