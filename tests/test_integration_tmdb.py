import pytest

from services.exceptions import TMDBAuthError
from services.tmdb_client import TMDBClient
from services.converter import convert_results
from models.search_result import SearchResult
from services.exceptions import TMDBConnectionError

#Real call: a bad API key should come back from TMDB as a 401 and become TMDBAuthError
@pytest.mark.integration
def test_real_invalid_api_key_raises_auth_error():
    client = TMDBClient(api_key="bad_key_for_integration_test")

    try:
        with pytest.raises(TMDBAuthError) as exc_info:
            client.get_movie_details(557)
    except TMDBConnectionError:
        pytest.skip("TMDB unreachable, cannot run this integration test")

    assert exc_info.value.status_code == 401
    assert "api key" in str(exc_info.value).lower()
    assert "bad_key_for_integration_test" not in str(exc_info.value)

#Real 404 Integration Test
@pytest.mark.integration
def test_real_nonexistent_movie_returns_none():
    client = TMDBClient() #real key from .env

    try:
        result = client.get_movie_details(999999999)
    except TMDBConnectionError:
        pytest.skip("TMDB unreachable, cannot run this integration test")

    assert result is None

#Real Integration Search
@pytest.mark.integration
def test_real_search_returns_search_result():
    client = TMDBClient()

    try:
        raw = client.search_multi("spiderman")
    except TMDBConnectionError:
        pytest.skip("TMDB unreachable, cannot run this integration test")

    result = convert_results(raw)

    assert len(result) > 0
    assert all(isinstance(item, SearchResult) for item in result)
    assert all(item.media_type in {"movie", "tv", "person"} for item in result)