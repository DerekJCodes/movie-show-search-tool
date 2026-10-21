import pytest
from services.exceptions import TMDBRateLimitError, TMDBAuthError, TMDBServerError, TMDBConnectionError
from cli import friendly_error, format_results, run_search, format_details, run_details
from models.search_result import SearchResult
from models.movie import Movie
from models.credits import Credits, CastMember
from main import main

class FakeClient:
    def search_multi(self, query):
        return {"results": [
            {"id": 1, "media_type": "movie", "title": "Spider-Man",
             "release_date": "2002-05-01", "vote_average": 7.4},
        ]}

class FakeEmptyClient:
    def search_multi(self, query):
        return {"results": []}

class RateLimitedClient:
    def search_multi(self, query):
        raise TMDBRateLimitError("rate limit", status_code=429, retry_after=30)

class FakeDetailsClient:
    def get_movie_details(self, movie_id):
        return Movie(id=movie_id, title="Spider-Man", release_date="2002-05-01",
                     vote_average=7.4, runtime=121,
                     overview="A student gets spider powers.", poster_path=None)
    def get_movie_credits(self, movie_id):
        return Credits(cast=[CastMember(1, "Tobey Maguire", "Peter Parker", None)],
                       crew=[])

class FakeNotFoundClient:
    def get_movie_details(self, movie_id):
        return None
    def get_movie_credits(self, movie_id):
        return None

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

    assert format_results(results) == "1. [Movie] Spider-Man (2002) - Rating: 7.4 - id: 1"

def test_format_results_tv_line():
    results = [SearchResult({
        "id": 2, "media_type": "tv", "name": "Breaking Bad",
        "first_air_date": "2008-01-20", "vote_average": 8.9,
    })]

    assert format_results(results) == "1. [TV] Breaking Bad (2008) - Rating: 8.9 - id: 2"

def test_format_results_numbers_multiple_results():
    results = [
        SearchResult({"id": 1, "media_type": "movie", "title": "A",
                      "release_date": "2001-01-01", "vote_average": 7.0}),
        SearchResult({"id": 2, "media_type": "tv", "name": "B",
                      "first_air_date": "2002-01-01", "vote_average": 8.0}),
    ]

    assert format_results(results) == (
        "1. [Movie] A (2001) - Rating: 7.0 - id: 1\n"
        "2. [TV] B (2002) - Rating: 8.0 - id: 2"
    )

def test_format_results_person_line_has_no_date_or_rating():
    results = [SearchResult({
        "id": 3, "media_type": "person", "name": "Tobey Maguire",
    })]

    assert format_results(results) == "1. [Person] Tobey Maguire - id: 3"

def test_format_results_missing_rating_shows_na():
    results = [SearchResult({
        "id": 4, "media_type": "movie", "title": "Unknown Film",
        "release_date": "2020-01-01",
    })]

    assert format_results(results) == "1. [Movie] Unknown Film (2020) - Rating: N/A - id: 4"

def test_run_search_formats_results():
    output = run_search(FakeClient(), "spiderman")

    assert output == "1. [Movie] Spider-Man (2002) - Rating: 7.4 - id: 1"

def test_run_search_formats_no_results():
    output = run_search(FakeEmptyClient(), "spiderman")

    assert output == "No results found."

def test_main_search_prints_results(capsys):
    exit_code = main(["search", "spiderman"], client=FakeClient())

    captured = capsys.readouterr()
    assert "Spider-Man" in captured.out
    assert exit_code == 0
def test_format_results_rounds_rating_to_one_decimal():
    results = [SearchResult({"id": 1, "media_type": "movie", "title": "A",
                             "release_date": "2001-01-01", "vote_average": 8.472})]

    assert "Rating: 8.5" in format_results(results)

def test_main_prints_friendly_error_and_returns_1(capsys):
    exit_code = main(["search", "spiderman"], client=RateLimitedClient())

    captured = capsys.readouterr()
    assert "30 seconds" in captured.err
    assert exit_code == 1
    assert captured.out == ""

def test_main_usage_goes_to_stderr(capsys):
    exit_code = main(["search"], client=FakeClient())

    captured = capsys.readouterr()
    assert "Usage" in captured.err
    assert captured.out == ""
    assert exit_code == 1

def test_format_results_empty_date_has_no_parentheses():
    results = [SearchResult({"id": 5, "media_type": "movie", "title": "Untitled",
                             "release_date": "", "vote_average": 7.0})]

    assert format_results(results) == "1. [Movie] Untitled - Rating: 7.0 - id: 5"

def test_format_results_zero_rating_shows_na():
    results = [SearchResult({"id": 6, "media_type": "movie", "title": "Unrated",
                             "release_date": "2020-01-01", "vote_average": 0})]

    assert format_results(results) == "1. [Movie] Unrated (2020) - Rating: N/A - id: 6"

def test_format_details_movie():
    movie = Movie(id=557, title="Spider-Man", release_date="2002-05-01",
                  vote_average=7.4, runtime=121,
                  overview="A student gets spider powers.", poster_path=None)
    credits = Credits(
        cast=[CastMember(1, "Tobey Maguire", "Peter Parker", None),
              CastMember(2, "Willem Dafoe", "Norman Osborn", None)],
        crew=[],
    )
    assert format_details(movie, credits) == (
            "Spider-Man (2002)\n"
            "Rating: 7.4 | Runtime: 121 min\n"
            "\n"
            "A student gets spider powers.\n"
            "\n"
            "Top cast: Tobey Maguire, Willem Dafoe"
        )

def test_format_details_missing_fields():
    movie = Movie(id=1, title="Obscure", release_date="",
                  vote_average=0, runtime=0,
                  overview="", poster_path=None)
    movie_credits = Credits(cast=[], crew=[])

    assert format_details(movie, movie_credits) == (
        "Obscure \n"
        "Rating: N/A | Runtime: N/A\n"
        "\n"
        "No overview available.\n"
        "\n"
        "Top cast: N/A"
    )

def test_run_details_movie():
    output = run_details(FakeDetailsClient(), "movie", 557)

    assert output.startswith("Spider-Man (2002)")
    assert "Top cast: Tobey Maguire" in output

def test_run_details_not_found():
    output = run_details(FakeNotFoundClient(), "movie", 999)

    assert output == "No movie found with id 999."