import sys
sys.path.append('../../')
from loader import load_from_xcpc_board_offline
from entities import *

competition_name, results = load_from_xcpc_board_offline('./ranklist.json', './teams.json')
print(competition_name)
print('Team count: {}'.format(len(results)))
print('Champion: {}'.format(results[0]))
print('Official Champion: {}'.format(list(filter(lambda x: x.is_official, results))[0]))