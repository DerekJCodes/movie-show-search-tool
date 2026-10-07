import pytest

from models.movie import Movie
from models.tv_show import TVShow
from services.tmdb_client import TMDBClient
from unittest.mock import Mock

@pytest.fixture
def tmdb_client():
    return TMDBClient(api_key="dummy")

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
            status_code = 200
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
            def __init__(self):
                self.status_code = 200
            def raise_for_status(self): pass
            def json(self): return {"OK": True}
        return FakeResponse()

    monkeypatch.setattr("requests.get", mock_get)
    client = TMDBClient(api_key="FAKE_API_KEY")

    client.search_multi("Regular Show")

    assert captured_url == "https://api.themoviedb.org/3/search/multi"
    assert captured_params["api_key"] == "FAKE_API_KEY"
    assert captured_params["query"] == "Regular Show"

def test_tmdb_client_raise_error_when_api_key_missing(monkeypatch):
    monkeypatch.delenv("TMDB_API_KEY", raising=False)
    with pytest.raises(ValueError) as exc_info:
        TMDBClient(api_key=None)

    assert "API Key" in str(exc_info.value)

def test_api_key_read_from_env(monkeypatch):
    monkeypatch.setenv("TMDB_API_KEY", "env_key")
    assert TMDBClient().api_key == "env_key"

@pytest.mark.parametrize("invalid_id",
                         [-1, 0, -999999, -1000000000,
                          "abc", "123", "1", "000",
                          None,
                          3.14, 3.0, 10.0,
                          {}, [], (1,), {1}, b"10", complex(1,2),
                          True
                          ])
def test_get_movie_details_invalid_id_raises_error(invalid_id):
    client = TMDBClient(api_key="dummy")

    with pytest.raises(ValueError) as exc_info:
        client.get_movie_details(invalid_id)

    assert "invalid movie id" in str(exc_info.value).lower()

def test_get_movie_details_nonexistent_id_returns_none(tmdb_client, mocker):
    mock_response = Mock(status_code=404, json=lambda: {})
    mocker.patch("requests.get", return_value=mock_response)

    result = tmdb_client.get_movie_details(999999999)
    assert result is None

#If no API key is passed
def test_missing_api_key_no_argument(monkeypatch):
    monkeypatch.delenv("TMDB_API_KEY", raising=False)

    with pytest.raises(ValueError):
        TMDBClient(api_key=None)

#If empty API string is passed
def test_missing_api_key_empty_string():
    with pytest.raises(ValueError):
        TMDBClient(api_key="")

#If .env isn't loading/env variable missing
def test_missing_api_key_env_var(monkeypatch):
    monkeypatch.delenv("TMDB_API_KEY", raising=False)

    with pytest.raises(ValueError):
        TMDBClient()

#If API key contains a whitespace
def test_missing_api_key_whitespace():
    with pytest.raises(ValueError):
        TMDBClient(api_key=" ")

#If TMDB endpoint is valid & is a movie (happy path)
def test_get_movie_details_success(monkeypatch, tmdb_client):
    fake_json = {
        "id": 123,
        "title": "Fake Movie",
        "release_date": "2024-01-01",
        "vote_average": 8.5,
        "runtime": 120,
        "overview": "Fake Movie Overview",
        "poster_path": "/poster.jpg"
    }

    def mock_get(url, params):
        class FakeResponse:
            status_code = 200
            def raise_for_status(self): pass
            def json(self): return fake_json
        return FakeResponse()

    monkeypatch.setattr("requests.get", mock_get)

    data = tmdb_client.get_movie_details(123)

    assert isinstance(data, Movie)
    assert data.id == 123
    assert data.title == "Fake Movie"

@pytest.mark.parametrize("invalid_id", [
    -1, 0, -999999, -1000000000,
    "abc", "invalid", None,
    3.14, 3.0, 10.0,
    (1+2j), True
])
def test_get_tv_details_invalid_id_raises_error(tmdb_client, invalid_id):

    with pytest.raises(ValueError) as exc_info:
        tmdb_client.get_tv_details(invalid_id)

def test_get_tv_details_nonexistent_id_returns_none(tmdb_client, mocker):
    mock_response = Mock(status_code=404, json=lambda: {})
    mocker.patch("requests.get", return_value=mock_response)

    result = tmdb_client.get_tv_details(999999999)
    assert result is None

def test_get_tv_details_success(monkeypatch, tmdb_client):
    fake_json = {
        "id": 1399,
        "name": "Game of Thrones",
        "overview": "Nine noble families fight for control over Westeros."
    }

    def mock_get(url, params):
        class FakeResponse:
            status_code = 200
            def raise_for_status(self): pass
            def json(self): return fake_json
        return FakeResponse()

    monkeypatch.setattr("requests.get", mock_get)

    data = tmdb_client.get_tv_details(1399)

    assert isinstance(data, TVShow)
    assert data.id == 1399
    assert data.name == "Game of Thrones"
