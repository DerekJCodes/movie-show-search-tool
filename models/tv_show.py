class TVShow:
    """A TV show, as returned by TMDB's /tv/{id} endpoint."""
    def __init__(self,
                 id: int,
                 name: str,
                 first_air_date: str,
                 vote_average: float,
                 overview: str,
                 poster_path: str | None,
                 number_of_seasons: int,
                 number_of_episodes: int):
        self.id = id
        self.name = name
        self.first_air_date = first_air_date
        self.vote_average = vote_average #vote_average is 0 when there are no votes
        self.overview = overview
        self.poster_path = poster_path
        self.number_of_seasons = number_of_seasons
        self.number_of_episodes = number_of_episodes
        self.media_type = "tv" #Lets the CLI tell TV shows from movies
