from models.movie import Movie
from models.credits import CastMember, CrewMember, Credits
from models.tv_show import TVShow

sample_json = {
    "cast": [
        {
            "id": 113,
            "name": "Tobey Maguire",
            "character": "Peter Parker / Spider-Man",
            "profile_path": "/path.jpg"
        }
    ],
    "crew": [
        {
            "id": 7624,
            "name": "Sam Raimi",
            "job": "Director",
            "department": "Directing",
            "profile_path": "/path.jpg"
        }
    ]
}

def parse_movie(json_data):
    return Movie(
        id=json_data.get("id"),
        title=json_data.get("title"),
        release_date=json_data.get("release_date"),
        vote_average=json_data.get("vote_average"),
        runtime=json_data.get("runtime"),
        overview=json_data.get("overview"),
        poster_path=json_data.get("poster_path"),
    )

def parse_show(json_data):
    return TVShow(
        id = json_data.get("id"),
        name=json_data.get("name"),
        first_air_date=json_data.get("first_air_date"),
        vote_average=json_data.get("vote_average"),
        number_of_episodes=json_data.get("number_of_episodes"),
        number_of_seasons=json_data.get("number_of_seasons"),
        overview=json_data.get("overview"),
        poster_path=json_data.get("poster_path")
    )

def parse_credits(json_data):
    cast_list = []
    crew_list = []

    for c in json_data.get("cast", []):
        cast_list.append(
            CastMember(
                id=c.get("id"),
                name=c.get("name"),
                character=c.get("character"),
                profile_path=c.get("profile_path")
            )
        )

    for c in json_data.get("crew", []):
        crew_list.append(
            CrewMember(
                id=c.get("id"),
                name=c.get("name"),
                job=c.get("job"),
                department=c.get("department"),
                profile_path=c.get("profile_path")
            )
        )

    return Credits(cast_list, crew_list)

credits = parse_credits(sample_json)

print(credits.cast[0].name)
print(credits.crew[0].job)
