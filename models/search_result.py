class SearchResult:
    """One item from a search/multi response: a movie/TV show or person.

    TMDB names the fields differently for each type (movies use title and
    release_date, TV uses name and first_air_date, people have only 'name'),
    so they are normalized here into .title and .date. People get date=None.
    """
    def __init__(self, raw):
        self.id = raw.get("id")
        self.media_type = raw.get("media_type")
        self.overview = raw.get("overview")
        self.poster_path = raw.get("poster_path")
        self.vote_average= raw.get("vote_average")
        self.genre_ids = raw.get("genre_ids")

        if self.media_type == "movie":
            self.title = raw.get("title")
            self.date = raw.get("release_date")
        elif self.media_type == "tv":
            self.title = raw.get("name")
            self.date = raw.get("first_air_date")
        else:
            self.title = raw.get("name")
            self.date = None

    def __str__(self):
        rating = f"{self.vote_average:.1f}" if self.vote_average is not None else "N/A"
        return f"{self.title} ({self.media_type}): - Rating: {rating} - id: {self.id}"