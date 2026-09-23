from models.credits import CastMember, CrewMember, Credits
from services.parsers import parse_credits, sample_json


def test_parse_credits():
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

credits = parse_credits(sample_json)

assert len(credits.cast) == 1
assert isinstance(credits.cast[0], CastMember)
assert credits.cast[0].name == "Tobey Maguire"
assert credits.cast[0].character == "Peter Parker / Spider-Man"

assert len(credits.crew) == 1
assert isinstance(credits.crew[0], CrewMember)
assert credits.crew[0].name == "Sam Raimi"
assert credits.crew[0].job == "Director"
assert credits.crew[0].department == "Directing"

