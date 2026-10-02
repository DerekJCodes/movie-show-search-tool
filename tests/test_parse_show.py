from models.tv_show import TVShow
from services.parsers import parse_show


def test_parse_show():
    sample_json = {
        "id": 1396,
        "name": "Breaking Bad",
        "first_air_date": "2008-01-20",
        "vote_average": 9.5,
        "number_of_seasons": 5,
        "number_of_episodes": 62,
        "overview": "A chemistry teacher turns to crime.",
        "poster_path": "/breakingbad.jpg"
    }

    show = parse_show(sample_json)

    assert isinstance(show, TVShow)
    assert show.id == 1396
    assert show.name == "Breaking Bad"
    assert show.number_of_seasons == 5
    assert show.number_of_episodes == 62