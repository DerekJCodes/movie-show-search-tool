from models.credits import Credits, CastMember, CrewMember

def test_credits_container():
    cast = [
        CastMember(
            id=113,
            name="Tobey Maguire",
            character="Peter Parker",
            profile_path="/path.jpg"
        )
    ]

    crew = [
        CrewMember(
            id=7624,
            name="Sam Raimi",
            job="Director",
            department="Directing",
            profile_path="/raimi.jpg"
        )
    ]

    credits = Credits(cast=cast, crew=crew)

    # Validate cast list
    assert len(credits.cast) == 1
    assert isinstance(credits.cast[0], CastMember)
    assert credits.cast[0].name == "Tobey Maguire"

    # Validate crew list
    assert len(credits.crew) == 1
    assert isinstance(credits.crew[0], CrewMember)
    assert credits.crew[0].job == "Director"
    assert credits.crew[0].department == "Directing"
