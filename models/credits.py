#Where majority of the casting crew are going to be listed based on their role: cast/crew & generalized credits with their name & role

class CastMember:
    def __init__(self, id, name, character, profile_path):
        self.id = id
        self.name = name
        self.character = character
        self.profile_path = profile_path

class CrewMember:
    def __init__(self, id, name, job, department, profile_path):
        self.id = id
        self.name = name
        self.job = job
        self.department = department
        self.profile_path = profile_path

class Credits:
    def __init__(self, cast, crew):
        self.cast = cast
        self.crew = crew