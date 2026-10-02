from models.movie import Movie
from models.credits import CastMember, CrewMember, Credits

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
