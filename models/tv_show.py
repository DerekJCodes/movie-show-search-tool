class TVShow:
    def __init__(self, id, name, first_air_date, vote_average, overview, poster_path, genre_ids):
        self.id = id
        self.name = name
        self.first_air_date = first_air_date
        self.vote_average = vote_average
        self.overview = overview
        self.poster_path = poster_path
        self.genre_ids = genre_ids 
        self.media_type = "tv"

    def __str__(self):
        return f"{self.name} - {self.first_air_date} Seasons - Rating: {self.vote_average:.1f}"