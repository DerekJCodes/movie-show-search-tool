class Show:
    def __init__(self, title, seasons, rating, overview, poster_path=None, tmdb_id=None):
        self.title = title
        self.seasons = seasons
        self.rating = rating
        self.overview = overview
        self.poster_path = poster_path
        self.tmdb_id = tmdb_id #For ID reference 

    def __str__(self):
        return f"{self.title} - {self.seasons} Seasons - Rating: {self.rating:.1f}"