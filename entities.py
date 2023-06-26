from enum import Enum
# This class is used to represent a competition result record.
class Result:
    school = None
    team_name = None
    members = None
    competition_id = None
    rank = None
    is_official = None
    school_rank = None
    prize = None

    def __init__(self, school, team_name, members, competition_id, rank, is_official, school_rank=None, prize=None):
        self.school = school
        self.team_name = team_name
        self.members = members
        self.competition_id = competition_id
        self.rank = rank
        self.is_official = is_official
        self.school_rank = school_rank
        self.prize = prize

    def __str__(self):
        return '学校: {}, 队名: {}, 成员: {}, 赛站id: {}, 排名: {}, 队伍类型: {}, 学校排名: {}, 奖牌: {}'.format(
            self.school, self.team_name, self.members, self.competition_id, self.rank, '正式' if self.is_official else '打星', self.school_rank, self.prize)

# This Enum class is to represent the type of a team.
class TeamType(Enum):
    # 正式
    Official = 1,
    # 打星
    Unofficial = 2
