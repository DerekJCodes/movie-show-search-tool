import pytest
from models.search_result import SearchResult


def test_movie_result_normalizes_fields():
    r = SearchResult({"id": 1, "media_type": "movie", "title": "Inception",
                      "release_date": "2010-07-16", "vote_average": 8.4})
    assert r.title == "Inception"
    assert r.date == "2010-07-16"


def test_tv_result_normalizes_fields():
    r = SearchResult({"id": 2, "media_type": "tv", "name": "Breaking Bad",
                      "first_air_date": "2008-01-20"})
    assert r.title == "Breaking Bad"
    assert r.date == "2008-01-20"


def test_person_result_has_title_and_no_date():
    r = SearchResult({"id": 3, "media_type": "person", "name": "Bryan Cranston"})
    assert r.title == "Bryan Cranston"
    assert r.date is None


def test_missing_fields_become_none():
    r = SearchResult({"media_type": "movie"})
    assert r.id is None
    assert r.title is None
    assert r.vote_average is None


@pytest.mark.parametrize("rating, expected", [(8.46, "8.5"), (None, "N/A")])
def test_str_handles_missing_rating(rating, expected):
    r = SearchResult({"media_type": "movie", "title": "X", "vote_average": rating})
    assert expected in str(r)