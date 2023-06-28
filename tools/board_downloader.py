# %%
import sys, os
sys.path.append('..')

# %%
import requests, time, json
from selenium import webdriver
from selenium.webdriver.common.by import By
from loader import load_from_xcpc_board_offline


# %%
template_ranklist_uri = 'https://board.xcpcio.com/icpc/{}/{}?type=%E5%AF%BC%E5%87%BA%E6%A6%9C%E5%8D%95'
template_teams_uri = 'https://board.xcpcio.com/data//icpc/{}/{}/team.json?t={}'
force_mode = False
skip_validation = False

# %%
def fetch_ranklist(season, site):
    print('Fetching Ranklist From XCPC Board...')
    uri = template_ranklist_uri.format(season, site)
    print(uri)
    driver = webdriver.Chrome()
    driver.get(uri)
    time.sleep(2)
    data_format = driver.find_element(
        By.XPATH, '/html/body/center/div/div/div[6]/div/span[1]/input')
    if data_format is None:
        raise Exception('Cannot Find Data Format Selector')
    data_format.send_keys('Rank JSON\n')
    time.sleep(1)
    generate = driver.find_element(By.XPATH, '/html/body/center/div/div/button')
    if generate is None:
        raise Exception('Cannot Find Generate Button')
    generate.click()
    time.sleep(1)
    result = driver.find_element(By.XPATH, '/html/body/center/div/div/div[7]/span/textarea')
    if result is None:
        raise Exception('Cannot Find Result')
    result = result.text
    return result


# %%
def fetch_teams(season, site):
    print('Fetching Teams From XCPC Board...')
    now_ticks = int(time.time())
    uri = template_teams_uri.format(season, site, now_ticks)
    print(uri)
    response = requests.get(uri)
    if response.status_code != 200:
        print(response)
        raise Exception('Cannot Fetch Teams')
    return response.json()

# %%
def export_board(export_path, season, site):
    ranklist_path = export_path + '\\ranklist.json'
    teams_path = export_path + '\\teams.json'
    
    ranlist = fetch_ranklist(season, site)
    if force_mode and not os.path.exists(export_path):
        os.makedirs(export_path)
        print('Created Output Path: {}'.format(export_path))
        
    with open(ranklist_path, 'w', encoding='utf-8') as f:
        f.write(ranlist)
    print('Ranklist Exported Successfully')

    teams = fetch_teams(season, site)
    with open(teams_path, 'w', encoding='utf-8') as f:
        json.dump(teams, f, ensure_ascii=False)
    print('Teams Exported Successfully')

    if skip_validation:
        return
    
    competition_name, results, error_list = load_from_xcpc_board_offline(ranklist_path, teams_path, safe_mode=True)
    print(competition_name)

    print('Team count: {}'.format(len(results)))
    print('Champion: {}'.format(results[0]))
    print('Official Champion: {}'.format(list(filter(lambda x: x.is_official, results))[0]))
    
    issues = []
    if results[0].members is None or len(results[0].members) == 0:
        issues.append('Empty Member Lists')

    issues = issues + error_list
    if len(issues) > 0:
        print('-----Issue Found-----')
        for issue in issues:
            print(issue)
        with open(export_path + '\\issues.txt', 'w', encoding='utf-8') as f:
            for issue in issues:
                f.write(issue + '\n')


# %%

if __name__ == '__main__':
    # Usage: 
    # output_folder is the folder to store the output files.
    # season is the season of the competition. This should be the same as the category in the xcpc board website.
    # site is the site of the competition. This should be the same as the site in the xcpc board website.
    # --force is a boolean value. If it is true, the program will create the output_folder if it is not exist and overwrite the existing files.
    # --skip_validation is a boolean value. If it is true, the program will skip the validation of the output files.
    # --help will print the usage.

    #output help info
    if len(sys.argv) == 1 or sys.argv[1] == '--help':
        print('Usage: python board_downloader.py output_folder season site [--force] [--skip_validation]')
        print('Example: python board_downloader.py ./board_data/47th/ec-final 47th ec-final --force')
        exit(0)
    
    #validate arguments
    if len(sys.argv) < 4: 
        print('Invalid Arguments')
        print('Use --help to see the usage')
        exit(1)
    
    #parse arguments
    output_folder = sys.argv[1]
    season = sys.argv[2]
    site = sys.argv[3]
    force_mode = '--force' in sys.argv
    skip_validation = '--skip_validation' in sys.argv

    if force_mode:
        print('Force Mode Enabled')
    
    #export board
    export_board(output_folder, season, site)
        
   

    

#export_board('./board_data/47th/ec-final', '47th', 'ec-final')


