import pytest
from services.exceptions import TMDBRateLimitError, TMDBAuthError, TMDBServerError, TMDBConnectionError
from cli import friendly_error

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