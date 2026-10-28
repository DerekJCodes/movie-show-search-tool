import os
import requests
import logging
from dotenv import load_dotenv
from services.parsers import parse_credits, parse_movie, parse_show
from services.exceptions import TMDBAuthError, TMDBServerError, TMDBRateLimitError, TMDBConnectionError

load_dotenv()

logger = logging.getLogger(__name__)

BASE_URL = "https://api.themoviedb.org/3"
def _error_message(response, default):
    """Use TMDB's own status_message if the body has one, otherwise the default."""
    try:
        return response.json().get("status_message", default)
    except ValueError:
        return default

def _retry_after_seconds(response):
    """Read Retry-After as whole seconds, or None if missing/not a number"""
    try:
        return int(response.headers.get("Retry-After"))
    except (TypeError, ValueError):
        return None

class TMDBClient:
    """
    Client for TMDB's search, details and credits endpoints.

    Every request goes through _get, which adds the API key and timeout, turns failures
    into our own exceptions, and logs the result
    """
    def __init__(self, api_key: str | None = None):
        key = api_key if api_key is not None else os.getenv("TMDB_API_KEY")
        if not key or not key.strip():
            raise ValueError("TMDB API key is required/missing")
        self.api_key = key.strip()

    def _get(self, endpoint: str, params: dict | None = None):
        """ Send a GET request to TMDB and return the decoded JSON

        Args:
            endpoint: Path after the base URL, e.g. "search/multi" or "movie/557"
            params: Extra query parameters. The API key is added to them.

        Returns:
            The decoded JSON body, or None if TMDB returns 404 (a missing ID
            is a normal result, so it is not raised).

        Raises:
            TMDBConnectionError: Timeout/network failure
            TMDBAuthError: 401, bad/missing API key
            TMDBRateLimitError: 429, carries retry_after when TMDB sends it
            TMDBServerError: Any 5xx error
            requests.HTTPError: Any other 4xx (not wrapped in a custom exception yet)
        """
        url = f"{BASE_URL}/{endpoint}"
        params = params or {}
        params["api_key"] = self.api_key

        try:
            response = requests.get(url, params=params, timeout=10)
        except (requests.Timeout, requests.ConnectionError) as exc:
            #The key is in the query string, so log only the endpoint and the exception
            #class. The exception's own text can contain the full URL.
            logger.error("TMDB %s -> %s", endpoint, type(exc).__name__)
            raise TMDBConnectionError(
                "Could not reach TMDB (timeout/network error)"
            ) from None #The original error text includes the URL (and key)

        #404 means the ID doesn't exist, which is a normal result, so return None instead of
        #raising
        if response.status_code == 404:
            logger.info("TMDB %s -> 404 Not Found", endpoint)
            return None

        #If API key is invalid/unauthorized
        #Bad key breaks every request, so ERROR (a developer has to fix it)
        if response.status_code == 401:
            logger.error("TMDB %s -> %s", endpoint, response.status_code)
            raise TMDBAuthError(
                _error_message(response, "Invalid/unauthorized API key"),
                status_code=401
            )

        #If TMDB is having server-side errors (any 5xx)
        if response.status_code >= 500:
            logger.error("TMDB %s -> %s", endpoint, response.status_code)
            raise TMDBServerError(
                _error_message(response, "TMDB server error"),
                status_code=response.status_code
            )

        #If TMDB is having rate-limiting error (429)
        #Temporary and expected, so WARNING; retry_after says how long to wait
        if response.status_code == 429:
            retry_after = _retry_after_seconds(response)
            logger.warning("TMDB %s -> 429 rate limited (retry_after=%s)", endpoint, retry_after)
            raise TMDBRateLimitError(
                _error_message(response, "Rate limit exceeded, try again later"),
                status_code=429,
                retry_after = _retry_after_seconds(response)
            )

        #Raise for any other 4xx code errors. Logs response then lets response raise HTTPError
        if response.status_code >= 400:
            # Catch-all error log for all other 4xx error codes, haven't given a custom exception
            # yet
            logger.error("TMDB %s -> %s", endpoint, response.status_code)
        response.raise_for_status()

        logger.info("TMDB %s -> %s", endpoint, response.status_code)
        return response.json()

    def search_multi(self, query: str):
        params = {
            "query": query,
            "include_adult": False,
            "language": "en-US",
            "page": 1
        }
        return self._get("search/multi", params)

    def get_movie_credits(self, movie_id: int | str):
        # Reject bools explicitly: in Python True is an int, so isinstance(True, int)
        # passes and get_movie_credits(True) would silently request movie 1.
        if isinstance(movie_id, bool) or not isinstance(movie_id, int) or movie_id <= 0:
            raise ValueError("Invalid movie ID")

        data = self._get(f"movie/{movie_id}/credits")
        return parse_credits(data) if data is not None else None

    def get_movie_details(self, movie_id: int):
        #Same ID check as get_movie_credits
        if isinstance(movie_id, bool) or not isinstance(movie_id, int) or movie_id <= 0:
            raise ValueError("Invalid movie ID")

        endpoint = f"movie/{movie_id}"
        data = self._get(endpoint)
        return parse_movie(data) if data is not None else None

    def get_tv_credits(self, tv_id: int | str):
        # Same ID check as get_movie_credits
        if isinstance(tv_id, bool) or not isinstance(tv_id, int) or tv_id <= 0:
            raise ValueError("Invalid TV ID")

        data = self._get(f"tv/{tv_id}/credits")
        return parse_credits(data) if data is not None else None

    def get_tv_details(self, tv_id: int | str):
        # Same ID check as get_movie_credits
        if isinstance(tv_id, bool) or not isinstance(tv_id, int) or tv_id <= 0:
            raise ValueError("Invalid TV ID")

        endpoint = f"tv/{tv_id}"
        data = self._get(endpoint)

        return parse_show(data) if data is not None else None