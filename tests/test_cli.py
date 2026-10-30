import pytest
import sys
from services.exceptions import TMDBRateLimitError, TMDBAuthError, TMDBServerError, TMDBConnectionError
from cli import friendly_error, format_results, run_search, format_details, run_details
from models.search_result import SearchResult
from models.movie import Movie
from models.tv_show import TVShow
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
    def get_movie_details(self, movie_id):
        raise TMDBRateLimitError("rate limit", status_code=429, retry_after=30)
    def get_tv_details(self, tv_id):
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

class FakeTVClient:
    def get_tv_details(self, tv_id):
        return TVShow(id=tv_id, name="Breaking Bad", first_air_date="2008-01-20",
                      vote_average=9.0, overview="A teacher turns to crime.",
                      poster_path=None, number_of_seasons=5, number_of_episodes=62)

    def get_tv_credits(self, tv_id):
        return Credits(cast=[CastMember(1, "Bryan Cranston", "Walter White", None)],
                       crew=[])

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
    assert "search" in captured.err
    assert "details" in captured.err
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
        "Obscure\n"
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

def test_format_details_tv():
    show = TVShow(id=1396, name="Breaking Bad", first_air_date="2008-01-20",
                  vote_average=9.0, overview="A teacher turns to crime.",
                  poster_path=None, number_of_seasons=5, number_of_episodes=62)
    movie_credits = Credits(
        cast=[CastMember(1, "Bryan Cranston", "Walter White", None)],
        crew=[],
    )

    assert format_details(show, movie_credits) == (
        "Breaking Bad (2008)\n"
        "Rating: 9.0 | 5 seasons, 62 episodes\n"
        "\n"
        "A teacher turns to crime.\n"
        "\n"
        "Top cast: Bryan Cranston"
    )

def test_run_details_tv():
    output = run_details(FakeTVClient(), "tv", 1396)

    assert output.startswith("Breaking Bad (2008)")
    assert "5 seasons, 62 episodes" in output

def test_run_details_unknown_media_type_raises():
    with pytest.raises(ValueError):
        run_details(FakeDetailsClient(), "person", 1)

def test_main_details_prints_movie(capsys):
    exit_code = main(["details", "movie", "557"], client=FakeDetailsClient())

    captured = capsys.readouterr()
    assert "Spider-Man (2002)" in captured.out
    assert exit_code == 0

def test_main_details_non_numeric_id_prints_error(capsys):
    exit_code = main(["details", "movie", "abc"], client=FakeDetailsClient())

    captured = capsys.readouterr()
    assert "id" in captured.err.lower()
    assert captured.out == ""
    assert exit_code == 1

def test_main_details_prints_friendly_error_and_returns_1(capsys):
    exit_code = main(["details", "movie", "557"], client=RateLimitedClient())

    captured = capsys.readouterr()
    assert "30 seconds" in captured.err
    assert captured.out == ""
    assert exit_code == 1

def test_main_reads_sys_argv_when_no_argv_given(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["main.py"])

    exit_code = main(client=FakeClient())

    assert exit_code == 1
    assert "Usage" in capsys.readouterr().err

@pytest.mark.parametrize("number_of_seasons, number_of_episodes, expected", [
    (1 ,1, "1 season, 1 episode"),
    (2 , 2,"2 seasons, 2 episodes"),
    (1, 62, "1 season, 62 episodes"),
    (2, 1, "2 seasons, 1 episode"),
    (2,62, "2 seasons, 62 episodes"),
])
def test_tv_details_plural_seasons_and_episodes(number_of_seasons, number_of_episodes, expected):
    show = TVShow(id=1396, name="Breaking Bad",first_air_date="2008-01-20",
                  vote_average=9.0, overview="A teacher turns to crime.",
                  poster_path=None, number_of_seasons=number_of_seasons, number_of_episodes=number_of_episodes)

    movie_credits = Credits(
            cast=[CastMember(1, "Bryan Cranston", "Walter White", None)],
            crew=[],
        )

    assert format_details(show, movie_credits) == (
        "Breaking Bad (2008)\n"
        f"Rating: 9.0 | {expected}\n"
        "\n"
        "A teacher turns to crime.\n"
        "\n"
        "Top cast: Bryan Cranston"
    )