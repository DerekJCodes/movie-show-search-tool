import os
import requests
from dotenv import load_dotenv
from services.parsers import parse_credits

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

    def get_movie_credits(self, movie_id: int):
        data = self._get(f"movie/{movie_id}/credits")
        return parse_credits(data)

    def get_movie_details(self, movie_id: int):
        if type(movie_id) is not int or movie_id <= 0:
            raise ValueError("Invalid movie ID")

        endpoint = f"movie/{movie_id}"
        return self._get(endpoint)

    def get_tv_details(self, tv_id: int | str) -> dict | None:
        if type(tv_id) is not int or tv_id <= 0:
            raise ValueError("Invalid TV ID")

        endpoint = f"/tv/{tv_id}"
        return self._get(endpoint)