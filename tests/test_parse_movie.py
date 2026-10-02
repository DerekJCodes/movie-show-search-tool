from models.movie import Movie
from services.parsers import parse_movie

def test_parse_movie():
    sample_json = {
        "id": 557,
        "title": "Spider-Man",
        "release_date": "2002-05-01",
        "vote_average": 7.3,
        "runtime": 121,
        "overview": "Bitten by a radioactive spider...",
        "poster_path": "/abc123.jpg"
    }

    movie = parse_movie(sample_json)

    assert isinstance(movie, Movie)
    assert movie.id == 557
    assert movie.title == "Spider-Man"
    assert movie.runtime == 121