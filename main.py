#Imports go here

class Movie:
    def __init__(self, title, year, rating, overview, poster_path=None):
        self.title = title
        self.year = year
        self.rating = rating
        self.overview = overview
        self.poster_path = poster_path
    #Magic method of string to make data more readable
    def __str__(self):
        return f"{self.title} ({self.year}) - Rating: {self.rating:.1f}"

spider_man = Movie("Spider-Man: Brand New Day", 2026, 7.848, "Fighting crime full-time as " \
"Spider-Man in a world that doesn't remember him—and the pressure of seeing " \
"his old friends move on without him—sparks a change in Peter Parker he may " \
"not have the power to control. But that transformation might also be the only thing " \
"that can stop a shocking new threat to the city and those he loves - a powerful villain no one can even see.", None)

print(spider_man) #Output Spider-Man: Brand New Day (2026) - Rating 7.8