#Imports go here
from models.movie import Movie
from models.show import Show
from mock_data import mock_movies, mock_shows, mock_database

def main():
    print("Mock database loaded:")
    for item in mock_database:
        print(item)

if __name__ == "__main__":
    main()
