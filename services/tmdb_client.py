import os
import requests
from dotenv import load_dotenv
from services.parsers import parse_credits

load_dotenv()

BASE_URL = "https://api.themoviedb.org/3"

class TMDBClient:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("TMDB_API_KEY")
        if not self.api_key:
            raise ValueError("TMDB API Key is required/missing")

    def _get(self, endpoint: str, params: dict | None = None):
        url = f"{BASE_URL}/{endpoint}"
        params = params or {}
        params["api_key"] = self.api_key

        response = requests.get(url, params=params)
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
