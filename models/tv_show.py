class TVShow:
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
        self.vote_average = vote_average
        self.overview = overview
        self.poster_path = poster_path
        self.number_of_seasons = number_of_seasons
        self.number_of_episodes = number_of_episodes
        self.media_type = "tv"

    def __str__(self):
        return f"{self.name} - {self.first_air_date} - Rating: {self.vote_average:.1f}"