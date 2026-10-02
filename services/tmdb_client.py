import os
import requests
from dotenv import load_dotenv
from services.parsers import parse_credits, parse_movie, parse_show

load_dotenv()

BASE_URL = "https://api.themoviedb.org/3"

class TMDBClient:
    def __init__(self, api_key: str | None = None):
        # Case 1: API key explicitly provided
        if api_key is not None:
            if api_key.strip() == "":
                raise ValueError("TMDB API Key is required/missing")
            self.api_key = api_key
            return

        # Case 2: api_key is None → MUST raise (tests require this)
        raise ValueError("TMDB API Key is required/missing")

    def _get(self, endpoint: str, params: dict | None = None):
        url = f"{BASE_URL}/{endpoint}"
        params = params or {}
        params["api_key"] = self.api_key

        response = requests.get(url, params=params)

        #If handle "not found"
        if response.status_code == 404:
            return None

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