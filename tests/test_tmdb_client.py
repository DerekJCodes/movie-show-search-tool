import pytest
import requests
from services.tmdb_client import TMDBClient

def test_search_multi(monkeypatch):
    fake_json = {
        "page" : 1,
        "results" : [
            {"id": 1, "media_type": "movie", "title": "Fake Movie"},
            {"id": 2, "media_type": "tv", "title": "Fake Show"}
        ]
    }
    def mock_get(url, params):
        class FakeResponse:
            def raise_for_status(self): pass
            def json(self): return fake_json
        return FakeResponse()
    monkeypatch.setattr("requests.get", mock_get)

    client = TMDBClient(api_key="FAKE_API_KEY")

    data = client.search_multi("spider-man")

    assert "results" in data
    assert data["results"][0]["title"] == "Fake Movie"
    assert data["results"][1]["title"] == "Fake Show"

def test_get_correct_url(monkeypatch):
    captured_url = None
    captured_params = None

    def mock_get(url, params):
        nonlocal captured_url, captured_params
        captured_url = url
        captured_params = params

        class FakeResponse:
            def raise_for_status(self): pass
            def json(self): return {"OK": True}
        return FakeResponse()

    monkeypatch.setattr("requests.get", mock_get)
    client = TMDBClient(api_key="FAKE_API_KEY")

    client.search_multi("Regular Show")

    assert captured_url == "https://api.themoviedb.org/3/search/multi"
    assert captured_params["api_key"] == "FAKE_API_KEY"
    assert captured_params["query"] == "Regular Show"

def test_tmdb_client_raise_error_when_api_key_missing():
    with pytest.raises(ValueError) as exc_info:
        TMDBClient(api_key=None)

    assert "API Key" in str(exc_info.value)