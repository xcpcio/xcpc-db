# %%
import json
from entities import *

# %%
# {'contestName': '第 47 届国际大学生程序设计竞赛亚洲区域赛西安站（正式赛）',
#  'teams': [{'members': ['冯施源', '彭博', '钱易'],
#             'organization': '北京大学',
#             'name': '摆烂人',
#             'place': {'all': 1}}]
# }
def load_board_data(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    #print(data)
    competition_name = data['contestName']
    results = []
    for raw in data['teams']:
        members = raw['members']
        school = raw['organization']
        team_name = raw['name']
        rank = raw['place']['all']
        results.append(Result(school=school, members=members, team_name=team_name, rank=rank, is_official=False, competition_id=-1))
    return [competition_name, results]

# %%

def load_teams_data(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    #print(data)
    teams = {}
    for raw in data.values():
        teams[(raw['organization'], raw['name'])] = TeamType.Official if 'official' in raw else TeamType.Unofficial
    return teams

# %%
def load_from_xcpc_board_offline(ranklist_json_path, teams_json_path, safe_mode=False):
    # 加载榜单
    # 从XCPC Board导出的榜单json文件
    # https://board.xcpcio.com/icpc/47th/xian?type=%E5%AF%BC%E5%87%BA%E6%A6%9C%E5%8D%95
    competition_name, results = load_board_data(ranklist_json_path)

    # 加载队伍信息（是否打星）
    # XCPC teams endpoint返回的json response
    # https://board.xcpcio.com/data//icpc/47th/xian/team.json?t=1687781690
    teams = load_teams_data(teams_json_path)
    error_list = []
    for result in results:
        
        try:
            result.is_official = teams[(
                result.school, result.team_name)] == TeamType.Official
        except KeyError as error:
            if safe_mode:
                result.is_official = False
                error_list.append('Cannot Determine Team Type: {} {}'.format(result.school, result.team_name))
            else:
                raise error

    return [competition_name, results, error_list]



