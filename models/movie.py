class Movie:
    """A movie, as returned by TMDB's /movie/{id} endpoint."""
    def __init__(self,
                 id: int,
                 title: str,
                 release_date: str,
                 vote_average: float,
                 runtime: int,
                 overview: str,
                 poster_path: str | None,
                 ):
        self.id = id
        self.title = title
        self.release_date = release_date #A "YYYY-MM-DD" string that may be empty
        self.vote_average = vote_average #vote_average is 0 when there are no votes
        self.runtime = runtime #runtime is in minutes and may be missing
        self.overview = overview
        self.poster_path = poster_path
        self.media_type = "movie" #Lets the CLI tell movies from TV shows