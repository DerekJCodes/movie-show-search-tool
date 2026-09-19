class Movie:
    def __init__(self, title, year, rating, overview, poster_path=None, tmdb_id=None, collection_id=None):
        self.title = title
        self.year = year
        self.rating = rating
        self.overview = overview
        self.poster_path = poster_path
        self.tmdb_id = tmdb_id #For future ID reference
        self.collection_id = collection_id 
    #Magic method of string to make data more readable
    def __str__(self):
        return f"{self.title} ({self.year}) - Rating: {self.rating:.1f}"