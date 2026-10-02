class Movie:
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
        self.release_date = release_date
        self.vote_average = vote_average
        self.runtime = runtime
        self.overview = overview
        self.poster_path = poster_path
        self.media_type = "movie"
    #Magic method of string to make data more readable
    def __str__(self):
        return f"{self.title} ({self.release_date}) - Rating: {self.vote_average:.1f}"