import os
import requests
from dotenv import load_dotenv
from services.parsers import parse_credits

load_dotenv()

BASE_URL = "https://api.themoviedb.org/3"
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

def search_multi(query):
    url = f"{BASE_URL}/search/multi"
    params = {
        "api_key": TMDB_API_KEY,
        "query": query,
        "include_adult": False,
        "language": "en-US",
        "page": 1
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def get_movie_credits(self, movie_id):
    url=f"{BASE_URL}/movie/{movie_id}/credits"
    data = self._get(url)
    return parse_credits(data)
