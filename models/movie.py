class Movie:
    def __init__(self, id, title, release_date, vote_average, overview, poster_path, genre_ids):
        self.id = id
        self.title = title
        self.release_date = release_date
        self.vote_average = vote_average
        self.overview = overview
        self.poster_path = poster_path
        self.genre_ids = genre_ids #For future ID reference
        self.media = "movie"
    #Magic method of string to make data more readable
    def __str__(self):
        return f"{self.title} ({self.release_date}) - Rating: {self.vote_average:.1f}"