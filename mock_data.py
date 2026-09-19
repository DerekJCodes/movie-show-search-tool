from models.movie import Movie
from models.show import Show

mock_movies = [
    Movie(
        "Spider-Man: Brand New Day",
        2026,
        7.848,
        "Fighting crime full-time as Spider-Man in a world that doesn't remember him...",
        None,
        tmdb_id=123456,
        collection_id=None
    ),
    Movie(
        "Inception",
        2010,
        8.8,
        "A thief who steals corporate secrets through dream-sharing technology.",
        None,
        tmdb_id=27205,
        collection_id=None
    ),
    Movie(
        "The Dark Knight",
        2008,
        9.0,
        "Batman faces the Joker, a criminal mastermind who plunges Gotham into chaos.",
        None,
        tmdb_id=155,
        collection_id=263
    )
]

mock_shows = [
    Show(
        "Breaking Bad",
        5,
        9.5,
        "A chemistry teacher turns to crime.",
        None,
        tmdb_id=1396
    ),
    Show(
        "Stranger Things",
        4,
        8.7,
        "Kids uncover supernatural mysteries in Hawkins, Indiana.",
        None,
        tmdb_id=66732
    ),
    Show(
        "The Office",
        9,
        8.9,
        "A mockumentary on a group of typical office workers.",
        None,
        tmdb_id=2316
    )
]

mock_database = mock_movies + mock_shows