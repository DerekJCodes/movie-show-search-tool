from models.credits import Credits, CastMember


def test_cast_member():
    cast = CastMember(
        id = 113,
        name = "Tobey Maguire",
        character = "Peter Parker / Spider-Man",
        profile_path = "/path.jpg"
    )

    assert cast.id == 113
    assert cast.name == "Tobey Maguire"
    assert cast.character == "Peter Parker / Spider-Man"
    assert cast.profile_path == "/path.jpg"