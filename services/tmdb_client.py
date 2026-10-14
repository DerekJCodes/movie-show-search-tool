import os
import requests
from dotenv import load_dotenv
from services.parsers import parse_credits, parse_movie, parse_show
from services.exceptions import TMDBAuthError, TMDBServerError, TMDBRateLimitError, TMDBConnectionError

load_dotenv()

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
    def __init__(self, api_key: str | None = None):
        key = api_key if api_key is not None else os.getenv("TMDB_API_KEY")
        if not key or not key.strip():
            raise ValueError("TMDB API key is required/missing")
        self.api_key = key.strip()

    def _get(self, endpoint: str, params: dict | None = None):
        url = f"{BASE_URL}/{endpoint}"
        params = params or {}
        params["api_key"] = self.api_key

        try:
            response = requests.get(url, params=params, timeout=10)
        except (requests.Timeout, requests.ConnectionError):
            raise TMDBConnectionError(
                "Could not reach TMDB (timeout/network error)"
            ) from None

        #If handle "not found"
        if response.status_code == 404:
            return None

        #If API key is invalid/unauthorized
        if response.status_code == 401:
            raise TMDBAuthError(
                _error_message(response, "Invalid/unauthorized API key"),
                status_code=401
            )

        #If TMDB is having server-side errors (any 5xx)
        if response.status_code >= 500:
            raise TMDBServerError(
                _error_message(response, "TMDB server error"),
                status_code=response.status_code
            )

        #If TMDB is having rate-limiting error (429)
        if response.status_code == 429:
            raise TMDBRateLimitError(
                _error_message(response, "Rate limit exceeded, try again later"),
                status_code=429,
                retry_after = _retry_after_seconds(response)
            )

        #Raise for all other error codes (for now)
        response.raise_for_status()

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
        if isinstance(movie_id, bool) or not isinstance(movie_id, int) or movie_id <= 0:
            raise ValueError("Invalid movie ID")

        data = self._get(f"movie/{movie_id}/credits")
        return parse_credits(data) if data is not None else None

    def get_movie_details(self, movie_id: int):
        if isinstance(movie_id, bool) or not isinstance(movie_id, int) or movie_id <= 0:
            raise ValueError("Invalid movie ID")

        endpoint = f"movie/{movie_id}"
        data = self._get(endpoint)
        return parse_movie(data) if data is not None else None

    def get_tv_credits(self, tv_id: int | str):
        if isinstance(tv_id, bool) or not isinstance(tv_id, int) or tv_id <= 0:
            raise ValueError("Invalid TV ID")

        data = self._get(f"tv/{tv_id}/credits")
        return parse_credits(data) if data is not None else None

    def get_tv_details(self, tv_id: int | str):
        if isinstance(tv_id, bool) or not isinstance(tv_id, int) or tv_id <= 0:
            raise ValueError("Invalid TV ID")

        endpoint = f"tv/{tv_id}"
        data = self._get(endpoint)

        return parse_show(data) if data is not None else None