class SearchResult:
    def __init__(self, raw):
        self.id = raw.get("id")
        self.media_type = raw.get("media_type")
        self.overview = raw.get("overview")
        self.poster_path = raw.get("poster_path")
        self.vote_average= raw.get("vote_average")
        self.genre_ids = raw.get("genre_ids")

        if self.media_type == "movie":
            self.title = raw.get("title")
            self.release_date = raw.get("release_date")
        elif self.media_type == "tv":
            self.name = raw.get("name")
            self.first_air_date = raw.get("first_air_date")