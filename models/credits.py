"""Cast and crew records, and the Credits container for one title."""

class CastMember:
    """A cast member. character is the role they played."""
    def __init__(self, id, name, character, profile_path):
        self.id = id
        self.name = name
        self.character = character
        self.profile_path = profile_path

class CrewMember:
    """A crew member. job is e.g. 'Director', department is e.g. 'Directing'."""
    def __init__(self, id, name, job, department, profile_path):
        self.id = id
        self.name = name
        self.job = job
        self.department = department
        self.profile_path = profile_path

class Credits:
    """The cast and crew of one title. cast is in billing order."""
    def __init__(self, cast, crew):
        self.cast = cast
        self.crew = crew