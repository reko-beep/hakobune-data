from models.characters import Character
from json import load, dump
from images.utils import ImageManipulation as img, add_cards



from utils import get_card_info, get_tables
from os.path import exists


def create_card_dict(rarity: int, img: str,  text: str, title: str):
    cards_bg = {
        'card_3': 'https://static.wikia.nocookie.net/gensin-impact/images/5/57/Rarity_3_background.png',
        'card_4': 'https://static.wikia.nocookie.net/gensin-impact/images/c/c9/Rarity_4_background.png',
        'card_5': 'https://static.wikia.nocookie.net/gensin-impact/images/e/ea/Rarity_5_background.png',
        'card_2': 'https://static.wikia.nocookie.net/gensin-impact/images/d/d4/Rarity_2_background.png',
        'card_1': 'https://static.wikia.nocookie.net/gensin-impact/images/6/69/Rarity_1_background.png',
        'card_0': 'https://static.wikia.nocookie.net/gensin-impact/images/6/69/Rarity_1_background.png'
    }
    
    return {
    "title": title,
    "img": img,
    "txt": text,
    "card_bg": cards_bg[f'card_{rarity}']
    }



ascension_template = {
    'talent_level_up_materials': 
        [
        {
            'rarity' : 2, 
            'amount' : 9,
        },
        
        {
            'rarity' : 3, 
            'amount' : 63,
        },
        {
            'rarity' : 4, 
            'amount' : 114,
        }
        ]
    ,
    'common_enemy_drops': [
        
        {
            'rarity' : 1, 
            'amount' : 36,
        },
        
        {
            'rarity' : 2, 
            'amount' : 96,
        },
        {
            'rarity' : 3, 
            'amount' : 129,
        }
        
    ]
    ,
    'weekly_boss_materials': [
        {
            'rarity': 5,
            'amount': 18
        }
    ],
    'common_boss_materials': [
        {
            'rarity': 4,
            'amount': 46
        }
    ],
    'ascension_gems': [
        {
            'rarity': 2,
            'amount': 1
        },
        {
            'rarity':3,
            'amount': 9
        },
        {
            'rarity':4,
            'amount': 9
        },
        {
            'rarity':5,
            'amount': 6
        }],
    'local_specialities': [
        {
            'rarity' : 0,
            'amount': 168
        }
    ],
    'common' : [
        {
            'rarity': 3,
            'name': 'mora',
            'amount': 7050*1000,
            'img': 'https://static.wikia.nocookie.net/gensin-impact/images/8/84/Item_Mora.png'
        },
        {
            'rarity': 4,
            'name' : 'heros wit',
            'amount': 419,
            'img': 'https://static.wikia.nocookie.net/gensin-impact/images/2/26/Item_Hero%27s_Wit.png'
        },
        {
            'rarity': 5,
            'name': 'crown of insight',
            'amount': 3,
            'img': 'https://static.wikia.nocookie.net/gensin-impact/images/0/04/Item_Crown_of_Insight.png'
            }
    ]
        
        
}


with open('materials.json', 'r') as f:
    data = load(f)

def get_ascension_card(type: str, name: str=''):
    cards_result = []
    cards_to_search = []
    series_search = False
    
    if type == 'common':
        for card in temp[type]:
            cards_result.append(
                create_card_dict(card['rarity'], card['img'], card['amount'], card['name'])
            )
    else:
        
        
        if type in ['talent_level_up_materials', 'common_enemy_drops', 'elite_enemy_drops', 'ascension_gems']:
            
            series = list(data[type].keys())
            for serie in series:
                if name.lower() in serie.lower():
                    cards_to_search = data[type][serie]
                    series_search = True
                    break
            
        else:
            
            cards_to_search = data[type]
            
        cards_template = temp[type]
        
        if len(cards_to_search) != 0:
            for rarity_card in cards_template:
                for card in cards_to_search:
                    if series_search:
                        if rarity_card['rarity'] == card['rarity']:
                            cards_result.append({**card, **{'txt': rarity_card['amount']}})
                    else:
                        if name.lower() in card['title'].lower() and rarity_card['rarity'] == card['rarity']:
                             cards_result.append({**card, **{'txt': rarity_card['amount']}})
                            
                        
    return cards_result
        





def create_ascension_card(character_name: str, character_url, **kwargs):
    '''
    
    kwargs allowed
    
    
    'local_specialities'
    'common_boss_materials'
    'talent_level_up_materials'
    'weekly_boss_materials'
    'common_enemy_drops'
    'common'
    'custom'
    
    '''
    
    allowed_kwargs = ['ascension_gems', 'local_specialities', 'common_boss_materials', 'talent_level_up_materials', 'weekly_boss_materials', 'common_enemy_drops', 'common', 'custom']
    card = img.create_image_card_wh(character_name, character_url, 1620, 1080, False, True, 50, True, 'Ascension Materials')
    


     
    

    start_x = card.size[0] // 2 - 95
    start_y = 200   
    end_x = start_x + (112*5)
    
    
    max_cards = 5
    card_count = 0
    row = 1   
    print(max_cards)
    cards_list = []
    if kwargs.get('custom', None) != None:
        for c in kwargs.get('custom'):
            
            cards_list.append(create_card_dict(c['rarity'], c['img'], c['amount'], c['name']))
    
        kwargs.pop('custom')
        kwargs['custom'] = cards_list
    all_cards = []
    for key in allowed_kwargs:
        if key in kwargs and key != 'custom':
            cards = get_ascension_card(key, kwargs[key])
            all_cards += cards
    all_cards += cards_list
    end = (len(all_cards) // 5)+ 1
    
    for c in range(1, end + 1 , 1):
        list_ = all_cards[(c-1)*5  : (c * 5)]     
        print((c-1)*5,  c*5 , list_)
        card = img.paste_cards(card, (start_x, start_y+ ((c * 142) - 122)), (end_x, start_y + ((c * 142) - 122)), list_)
    
    remaining = all_cards[end * 5: ]
    print(remaining)
    card = img.paste_cards(card, (start_x, start_y+ ((end * 142) - 122)), (end_x, start_y + ((end * 142) - 122)), remaining)
    
    
        
                    

    
            
            

    

    card.save('test1.png')


create_ascension_card('Yaoyao', 'https://static.zerochan.net/Yaoyao.full.3841910.png', common='add', common_enemy_drops='slime', talent_level_up_materials='diligence',common_boss_materials='quelled', ascension_gems='nagadus', local_specialities='jueyun chili', weekly_boss_materials="daka's bell")