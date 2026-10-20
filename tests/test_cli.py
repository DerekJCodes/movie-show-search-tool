import pytest
from services.exceptions import TMDBRateLimitError, TMDBAuthError, TMDBServerError, TMDBConnectionError
from cli import friendly_error, format_results
from models.search_result import SearchResult

def test_rate_limit_message_includes_wait_time():
    err = TMDBRateLimitError("rate limit", status_code=429, retry_after=30)

    assert "30 seconds" in friendly_error(err)

def test_rate_limit_message_includes_no_wait_time():
    err = TMDBRateLimitError("rate limit", status_code=429)

    assert "Please wait a moment" in friendly_error(err)

def test_rate_limit_zero_wait_says_try_again_now():
    err = TMDBRateLimitError("rate limit", status_code=429, retry_after=0)

    assert "try again now" in friendly_error(err)

def test_unknown_exception_is_reraised():
    err = ValueError("something unexpected")

    with pytest.raises(ValueError):
        friendly_error(err)

def test_auth_error_message_points_to_env_var_and_hides_details():
    err = TMDBAuthError("Invalid API key: bad_key_123", status_code=401)

    result = friendly_error(err)

    assert "TMDB_API_KEY" in result
    assert "bad_key_123" not in result

def test_server_error_message():
    err = TMDBServerError("Server error", status_code=500)

    result = friendly_error(err)
    assert "TMDB is having trouble" in result

def test_connection_error_message():
    err = TMDBConnectionError("Connection error")

    result = friendly_error(err)

    assert "Check your internet connection" in result

def test_format_results_empty_list_says_no_results():
    assert "No results" in format_results([])

def test_format_results_movie_line():
    results = [SearchResult({
        "id": 1, "media_type": "movie", "title": "Spider-Man",
        "release_date": "2002-05-01", "vote_average": 7.4,
    })]

    assert format_results(results) == "1. [Movie] Spider-Man (2002) - Rating: 7.4"

def test_format_results_tv_line():
    results = [SearchResult({
        "id": 2, "media_type": "tv", "name": "Breaking Bad",
        "first_air_date": "2008-01-20", "vote_average": 8.9,
    })]

    assert format_results(results) == "1. [TV] Breaking Bad (2008) - Rating: 8.9"

def test_format_results_numbers_multiple_results():
    results = [
        SearchResult({"id": 1, "media_type": "movie", "title": "A",
                      "release_date": "2001-01-01", "vote_average": 7.0}),
        SearchResult({"id": 2, "media_type": "tv", "name": "B",
                      "first_air_date": "2002-01-01", "vote_average": 8.0}),
    ]

    assert format_results(results) == (
        "1. [Movie] A (2001) - Rating: 7.0\n"
        "2. [TV] B (2002) - Rating: 8.0"
    )

def test_format_results_person_line_has_no_date_or_rating():
    results = [SearchResult({
        "id": 3, "media_type": "person", "name": "Tobey Maguire",
    })]

    assert format_results(results) == "1. [Person] Tobey Maguire"

def test_format_results_missing_rating_shows_na():
    results = [SearchResult({
        "id": 4, "media_type": "movie", "title": "Unknown Film",
        "release_date": "2020-01-01",
    })]

    assert format_results(results) == "1. [Movie] Unknown Film (2020) - Rating: N/A"