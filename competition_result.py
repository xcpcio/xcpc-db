# This class is used to represent a competition result.
class Result:
    school = None
    team_name = None
    members = None
    competition_id = None
    rank = None
    is_official = None
    school_rank = None
    prize = None
    
    def __init__(self, school, team_name, members, competition_id, rank, is_official, school_rank = None, prize = None):
        self.school = school
        self.team_name = team_name
        self.members = members
        self.competition_id = competition_id
        self.rank = rank
        self.is_official = is_official
        self.school_rank = school_rank
        self.prize = prize