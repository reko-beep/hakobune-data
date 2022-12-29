
from utils import get_card_info, get_tables
from requests import get
from bs4 import BeautifulSoup
from os.path import exists
from json import load, dump


def save_talent_level_up_materials():
    data = {}
    if exists('materials.json'):
        with open('materials.json', 'r') as f:
            data = load(f)
        
    url = 'https://genshin-impact.fandom.com/wiki/Talent_Level-Up_Material'

    src = get(url).content

    bs = BeautifulSoup(src, 'lxml')
    
    tables = [get_tables(bs, 'Mondstadt', True)] + [get_tables(bs, 'Liyue', True)] + [get_tables(bs, 'Inazuma', True)] + [get_tables(bs, 'Sumeru', True)] 
    if len(tables) != 0:
        temp = dict()
        key = ''        
        for table in tables:
            rows = table.find_all('tr')
            for row in rows[1:]:
                cols = row.find_all('td')[1]
                containers = [get_card_info(e) for e in cols.find_all('div', {'class': 'card_container'})]
                if len(containers) != 0:
                    key = cols.find('a').attrs['title'].lower().replace('books','', 1).strip()
                    temp[key] = containers
        new_data = temp
        if 'talent_level_up_materials' in data:
            new_data = {new : temp[new] for new in temp if new not in data['talent_level_up_materials']}
            check = True if len(new_data) != 0 else False
            print('New talent level up materials', check)
        else:
            data['talent_level_up_materials'] = {}
        data['talent_level_up_materials'] = {**data['talent_level_up_materials'], **new_data}
     
    table = get_tables(bs, 'Weekly_Boss_Drops', True)
    rows = table.find_all('tr')
    temp = []
    for row in rows[1:]:
    
        cols = row.find_all('td')[1] if len(row.find_all('td')) == 3 else row.find_all('td')[0]
        containers = [get_card_info(e) for e in cols.find_all('div', {'class': 'card_container'})]
        temp += containers
    new_data = temp
    if 'weekly_boss_materials' in data:
        new_data = [new for new in temp if new not in data['weekly_boss_materials']]
        check = True if len(new_data) != 0 else False
        print('New boss materials', check)
    else:
        data['weekly_boss_materials'] = []
    data['weekly_boss_materials'] += new_data


    with open('materials.json', 'w') as f:
        dump(data, f, indent=1)

def save_character_ascension_materials():
    data = {}
    if exists('materials.json'):
        with open('materials.json', 'r') as f:
            data = load(f)
        
    url = 'https://genshin-impact.fandom.com/wiki/Character_Ascension_Material'

    src = get(url).content

    bs = BeautifulSoup(src, 'lxml')
    
    table = get_tables(bs, 'Ascension_Gems', True)
    rows = table.find_all('tr')
    temp = {}
    
    for row in rows[1:]:
    
        cols = row.find_all('td')[0]
        key = cols.find('a').attrs['title'].lower()
            
        containers = [get_card_info(e) for e in cols.find_all('div', {'class': 'card_container'})]
        temp[key] = containers        
    new_data = temp
    if 'ascension_gems' in data:
        new_data = {new : temp[new] for new in temp if new not in data['ascension_gems']}
        check = True if len(new_data) != 0 else False
        print('New  ascension gems', check)
    else:
        data['ascension_gems'] = {}
    data['ascension_gems'] = {**data['ascension_gems'], **new_data}
    
    table = get_tables(bs, 'Normal_Boss_Drops', True)
    rows = table.find_all('tr')
    temp = []
    for row in rows[1:]:
    
        cols = row.find_all('td')[0]
        containers = [get_card_info(e) for e in cols.find_all('div', {'class': 'card_container'})]
        temp += containers
    new_data = temp
    if 'common_boss_materials' in data:
        new_data = [new for new in temp if new not in data['common_boss_materials']]
        check = True if len(new_data) != 0 else False
        print('New common boss materials', check)
    else:
        data['common_boss_materials'] = []
    data['common_boss_materials'] += new_data  
    
  
    
    
    tables = [get_tables(bs, 'Mondstadt', True)] + [get_tables(bs, 'Liyue', True)] + [get_tables(bs, 'Inazuma', True)] + [get_tables(bs, 'Sumeru', True)] 
    if len(tables) != 0:
        temp = []
        for table in tables:
            rows = table.find_all('tr')
            for row in rows[1:]:
                cols = row.find_all('td')[0]
                containers = [get_card_info(e) for e in cols.find_all('div', {'class': 'card_container'})]
                temp += containers
        new_data = temp
        if 'local_specialities' in data:
            new_data = [new for new in temp if new not in data['local_specialities']]
            check = True if len(new_data) != 0 else False
            print('New local specialities', check)
        else:
            data['local_specialities'] = []
        data['local_specialities'] += new_data
    
    with open('materials.json', 'w') as f:
        dump(data, f, indent=1)

def save_common_ascension_materials():
    data = {}
    if exists('materials.json'):
        with open('materials.json', 'r') as f:
            data = load(f)
        
    url = 'https://genshin-impact.fandom.com/wiki/Common_Ascension_Material'


    src = get(url).content

    bs = BeautifulSoup(src, 'lxml')
    
    table = get_tables(bs, 'General_Enemy_Drops', True)
    rows = table.find_all('tr')
    temp = {}
    for row in rows[1:]:
        
        print(len(row.find_all('td')), len(row.find_all('td')) == 3)
        if len(row.find_all('td')) == 2:
            cols = row.find_all('td')[0]
            key = row.find('th').text.strip().lower() 
            containers = [get_card_info(e) for e in cols.find_all('div', {'class': 'card_container'})]
            temp[key] = containers
    new_data = temp
    if 'common_enemy_drops' in data:
        new_data = {new: temp[new] for new in temp if new not in data['common_enemy_drops']}
        check = True if len(new_data) != 0 else False
        print('New common enemies', check)
    else:
        data['common_enemy_drops'] = {}
    data['common_enemy_drops'] = {**data['common_enemy_drops'], **new_data}
    
    table = get_tables(bs, 'Elite_Enemy_Drops', True)
    rows = table.find_all('tr')
    temp = {}
    for row in rows[1:]:
        print(len(row.find_all('td')))
        cols = row.find_all('td')[0]
        key = row.find('th').text.strip().lower()
        containers = [get_card_info(e) for e in cols.find_all('div', {'class': 'card_container'})]
        temp[key] = containers
    new_data = temp
    if 'elite_enemy_drops' in data:
        new_data = {new: temp[new] for new in temp if new not in data['elite_enemy_drops']}
        check = True if len(new_data) != 0 else False
        print('New elite enemy drops', check)
    else:
        data['elite_enemy_drops'] = {}
    data['elite_enemy_drops'] = {**data['elite_enemy_drops'], **new_data  }
    
    with open('materials.json', 'w') as f:
        dump(data, f, indent=1)
  

