import pytest
import logging

from services.exceptions import TMDBRateLimitError, TMDBError
from services.tmdb_client import TMDBClient


@pytest.fixture
def tmdb_client():
    return TMDBClient(api_key='SECRET123')

def fake_response(status_code=200):
    class FakeResponse:
        url = "https://api.themoviedb.org/3/search/multi?api_key=SECRET123&query=spiderman"
        headers = {}
        def json(self):
            return {"results": []}
        def raise_for_status(self):
            pass
    FakeResponse.status_code = status_code
    return FakeResponse()

def test_successful_search_logs_and_status(monkeypatch,caplog,tmdb_client):

    monkeypatch.setattr("requests.get", lambda *args, **kwargs: fake_response())
    caplog.set_level(logging.DEBUG)

    tmdb_client.search_multi("spiderman")
    assert "search/multi" in caplog.text
    assert "200" in caplog.text

def test_api_key_never_appears_in_logs(monkeypatch,caplog, tmdb_client):

    monkeypatch.setattr("requests.get", lambda *args, **kwargs: fake_response())
    caplog.set_level(logging.DEBUG)

    tmdb_client.search_multi("spiderman")

    assert "SECRET123" not in caplog.text

def test_rate_limit_logs_warning(monkeypatch, caplog, tmdb_client):
    monkeypatch.setattr("requests.get", lambda *args, **kwargs: fake_response(429))
    caplog.set_level(logging.DEBUG)

    with pytest.raises(TMDBRateLimitError):
        tmdb_client.search_multi("spiderman")

    records = [r for r in caplog.records if r.levelname == "WARNING"]
    assert len(records) == 1
    assert "429" in caplog.records[0].getMessage()
    assert "search/multi" in caplog.records[0].getMessage()
    assert "SECRET123" not in caplog.text

@pytest.mark.parametrize("status", [401, 500, 503])
def test_error_responses_log_error(monkeypatch, caplog, tmdb_client, status):
    monkeypatch.setattr("requests.get", lambda *args, **kwargs: fake_response(status))
    caplog.set_level(logging.DEBUG)

    with pytest.raises(TMDBError):
        tmdb_client.search_multi("spiderman")

    records = [r for r in caplog.records if r.levelname == "ERROR"]
    assert len(records) == 1
    assert str(status) in records[0].getMessage()
    assert "SECRET123" not in caplog.text


