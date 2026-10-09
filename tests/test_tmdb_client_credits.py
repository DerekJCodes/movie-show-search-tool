import pytest
import requests

from models.credits import Credits, CastMember, CrewMember
from services.converter import convert_results
from services.tmdb_client import TMDBClient

# Response shapes captured from real TMDB calls in Postman
NOT_FOUND_BODY = {
    "success": False,
    "status_code": 34,
    "status_message": "The resource you requested could not be found."
}

INVALID_KEY_BODY = {
    "success": False,
    "status_code": 7,
    "status_message": "Invalid API key: You must be granted a valid key."
}

CREDITS_BODY = {
    "id": 557,
    "cast": [
        {"adult": False, "gender": 2, "id": 113, "name": "Tobey Maguire",
         "popularity": 20.1, "profile_path": "/tobey.jpg", "cast_id": 10,
         "character": "Peter Parker / Spider-Man", "credit_id": "abc", "order": 0},
        {"adult": False, "gender": 1, "id": 999, "name": "Unknown Extra",
         "popularity": 0.5, "profile_path": None, "cast_id": 11,
         "character": "Bystander", "credit_id": "def", "order": 50}
    ],
    "crew": [
        {"adult": False, "gender": 2, "id": 7624, "name": "Sam Raimi",
         "department": "Directing", "job": "Director",
         "profile_path": "/raimi.jpg", "credit_id": "ghi"}
    ]
}

@pytest.fixture
def tmdb_client():
    return TMDBClient(api_key="dummy")

#If credits endpoint is valid (happy path)
@pytest.mark.parametrize("method", ["get_movie_credits", "get_tv_credits"])
def test_credits_success(monkeypatch, tmdb_client, method):
    def mock_get(url, params, **kwargs):
        class FakeResponse:
            status_code = 200
            def raise_for_status(self): pass
            def json(self): return CREDITS_BODY
        return FakeResponse()

    monkeypatch.setattr("requests.get", mock_get)

    data = getattr(tmdb_client, method)(557)

    assert isinstance(data, Credits)
    assert len(data.cast) == 2
    assert isinstance(data.cast[0], CastMember)
    assert data.cast[0].name == "Tobey Maguire"
    assert isinstance(data.crew[0], CrewMember)
    assert data.crew[0].job == "Director"

#If a cast member has no profile picture (real TMDB data has these)
def test_credits_missing_profile_path(monkeypatch, tmdb_client):
    def mock_get(url, params):
        class FakeResponse:
            status_code = 200
            def raise_for_status(self): pass
            def json(self): return CREDITS_BODY
        return FakeResponse()

    monkeypatch.setattr("requests.get", mock_get)

    data = tmdb_client.get_movie_credits(557)

    assert data.cast[1].profile_path is None

#If the ID doesn't exist, TMDB returns 404 and we return None
@pytest.mark.parametrize("method", ["get_movie_credits", "get_tv_credits",
                                    "get_movie_details", "get_tv_details"])
def test_not_found_returns_none(monkeypatch, tmdb_client, method):
    def mock_get(url, params, **kwargs):
        class FakeResponse:
            status_code = 404
            def raise_for_status(self): pass
            def json(self): return NOT_FOUND_BODY
        return FakeResponse()

    monkeypatch.setattr("requests.get", mock_get)

    assert getattr(tmdb_client, method)(999999999) is None

#If the ID is invalid, we raise before ever calling the API
@pytest.mark.parametrize("method", ["get_movie_credits", "get_tv_credits"])
@pytest.mark.parametrize("invalid_id", [0, -1, "abc", None, 3.5, True])
def test_credits_invalid_id_raises_error(monkeypatch, tmdb_client, method, invalid_id):
    calls = []

    def mock_get(url, params, **kwargs):
        calls.append(url)

    monkeypatch.setattr("requests.get", mock_get)

    with pytest.raises(ValueError):
        getattr(tmdb_client, method)(invalid_id)

    assert calls == []

#If the API key is invalid, TMDB returns 401 and we raise
def test_invalid_api_key_raises_http_error(monkeypatch, tmdb_client):
    def mock_get(url, params, **kwargs):
        class FakeResponse:
            status_code = 401
            def raise_for_status(self):
                raise requests.HTTPError("401 Client Error: Unauthorized")
            def json(self): return INVALID_KEY_BODY
        return FakeResponse()

    monkeypatch.setattr("requests.get", mock_get)

    with pytest.raises(requests.HTTPError):
        tmdb_client.get_movie_details(557)

#If TMDB is having issues(server problems, rate limiting), we raise
@pytest.mark.parametrize("status_code", [500,502,503,429])
def test_server_error_raises_http_error(monkeypatch, tmdb_client, status_code):
    def mock_get(url, params, **kwargs):
        class FakeResponse:
            status_code = 500
            def raise_for_status(self):
                if self.status_code >= 400:
                    raise requests.HTTPError(f"{self.status_code} Error")
            def json(self): return {}
        FakeResponse.status_code = status_code
        return FakeResponse()

    monkeypatch.setattr("requests.get", mock_get)

    with pytest.raises(requests.HTTPError):
        tmdb_client.search_multi("spiderman")

#If a search finds nothing, TMDB returns 200 with an empty list
def test_empty_search_results_convert_to_empty_list(monkeypatch, tmdb_client):
    fake_json = {"page": 1, "results": [], "total_pages": 1, "total_results": 0}

    def mock_get(url, params, **kwargs):
        class FakeResponse:
            status_code = 200
            def raise_for_status(self): pass
            def json(self): return fake_json
        return FakeResponse()

    monkeypatch.setattr("requests.get", mock_get)

    raw = tmdb_client.search_multi("")

    assert convert_results(raw) == []

def test_server_timeout(monkeypatch, tmdb_client):
    def mock_get(url, params, **kwargs):
        raise requests.Timeout()

    monkeypatch.setattr("requests.get", mock_get)
    with pytest.raises(requests.Timeout):
        tmdb_client.search_multi("spiderman")