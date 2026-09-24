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
