class TMDBError(Exception):
    """Base class for all errors raised by TMDBClient."""
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code

class TMDBAuthError(TMDBError):
    """The API key was missing, invalid, or not authorized (HTTP 401)."""

class TMDBServerError(TMDBError):
    """TMDB had a problem on its side (HTTP 5xx)."""

class TMDBRateLimitError(TMDBError):
    """Too many requests (HTTP 429)."""

class TMDBConnectionError(TMDBError):
    """TMDB couldn't be reached: timeout or network failure."""