class TMDBError(Exception):
    """Base class for the API and network failures TMDBClient turns into our
    own errors.

    Catch this to handle any of them at once. Bad IDs (ValueError) and
    other 4xx responses (requests.HTTPError) are not wrapped yet.
    """
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code

class TMDBAuthError(TMDBError):
    """The API key was missing, invalid, or not authorized (HTTP 401)."""

class TMDBServerError(TMDBError):
    """TMDB had a problem on its side (HTTP 5xx)."""

class TMDBRateLimitError(TMDBError):
    """Too many requests (HTTP 429).

    retry_after is the wait in whole seconds from TMDB's Retry-After header
    or None if TMDB didn't send one.
    """
    def __init__(self, message, status_code=None, retry_after=None):
        super().__init__(message, status_code)
        self.retry_after = retry_after

class TMDBConnectionError(TMDBError):
    """TMDB couldn't be reached: timeout or network failure.

    status_code is None, because no response was received.
    """