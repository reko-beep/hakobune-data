from string import punctuation
import fuzzywuzzy as fuzz
from json import dump
import typing

class CharacterEXPFilter:

    def __init__(self, level: typing.Union[range, int], card_exp_mat: list = ['hw', 'ae', 'wa']) -> None:
        self.level = level
        self.allowed_mats = [mat for mat in ['hw', 'ae', 'wa'] if mat in card_exp_mat]
        self.dict_ = {
                            "20": {
                            "xp_required": 120175,
                            "xp": 825,
                            "mora": 24200
                            },
                            "40": {
                            "xp_required": 578325,
                            "xp": 675,
                            "mora": 115800
                            },
                            "50": {
                            "xp_required": 579100,
                            "xp": 900,
                            "mora": 116000
                            },
                            "60": {
                            "xp_required": 854125,
                            "xp": 875,
                            "mora": 171000
                            },
                            "70": {
                            "xp_required": 1195925,
                            "xp": 75,
                            "mora": 239200
                            },
                            "80": {
                            "xp_required": 1611875,
                            "xp": 125,
                            "mora": 322400
                            },
                            "90": {
                            "xp_required": 8362650,
                            "xp": 4350,
                            "mora": 1673400
                            }
                        }
        self.card_bg = {
                'hw': 'https://static.wikia.nocookie.net/gensin-impact/images/c/c9/Rarity_4_background.png',
                'ae': 'https://static.wikia.nocookie.net/gensin-impact/images/5/57/Rarity_3_background.png',
                'wa': 'https://static.wikia.nocookie.net/gensin-impact/images/d/d4/Rarity_2_background.png',
                'mora' : 'https://static.wikia.nocookie.net/gensin-impact/images/6/69/Rarity_1_background.png'
            }
        self.mat_xp = {
                'hw': 20000,
                'ae': 5000,
                'wa': 1000
            }
        self.mat_mora = {
                'hw': 4000,
                'ae': 1000,
                'wa': 200
            }
        self.mat_text = {
            'hw': "Hero's Wit",
            'ae': "Adventurer's EXP",
            'wa': "Wanderer's Advice"
        }
        self.mat_img = {
            'hw': 'https://static.wikia.nocookie.net/gensin-impact/images/2/26/Item_Hero%27s_Wit.png',
            'ae': 'https://static.wikia.nocookie.net/gensin-impact/images/0/07/Item_Adventurer%27s_Experience.png',
            'wa': 'https://static.wikia.nocookie.net/gensin-impact/images/6/60/Item_Wanderer%27s_Advice.png',
            'mora': 'https://static.wikia.nocookie.net/gensin-impact/images/8/84/Item_Mora.png'
        }
        self.calc_data = {

        }
        self.calculate_mats()
        self.calculate_mora()

    def calculate_mats(self) -> tuple:

        mats = {'hw': 0, 'ae': 0, 'wa': 0}
        xp_req = 0

        if isinstance(self.level, range):
            for lvl in list(self.level):

                if str(lvl) in self.dict_:
                    xp_req += self.dict_[str(lvl)]['xp_required']
        else:

            xp_req = self.dict_[str(self.level)]['xp_required']
        xp_left = xp_req
        
        for mat in self.allowed_mats:

            
            mats[mat] = xp_left // self.mat_xp[mat]
            xp_left -= mats[mat] * self.mat_xp[mat]

        excess = {k : 0 for k in self.allowed_mats[::-1]}
        
        for mat in excess:            
            excess[mat] = self.mat_xp[mat] - xp_left
        
        excess_mat = min(excess, key=excess.get)
        mats[excess_mat] += 1
        xp_wasted = excess[excess_mat]


        self.calc_data = {**self.calc_data,
                            **mats}
        self.calc_data['xp_wasted'] = xp_wasted
        self.calc_data['xp_req'] = xp_req

      

    def calculate_mora(self):

        self.calc_data['mora'] = 0
        for mat in self.allowed_mats:

            if mat in self.calc_data:

                self.calc_data['mora'] += self.calc_data[mat] * self.mat_mora[mat]
        

    @property
    def data(self):
        data_dict = {

        }

        '''
        
        Without Card template

        '''
        data_dict['level'] = self.level
        for i in self.allowed_mats:
            data_dict[self.mat_text[i]] = self.calc_data[i]
        
        for i in ['xp_wasted', 'xp_req']:

            data_dict[i] = self.calc_data[i]
        
        if 'mora' in self.calc_data:
            data_dict['mora'] = self.calc_data['mora']



        return data_dict
    
    @property
    def cards(self):
        data_dict = {}
        '''
        
        With Card template

        '''
        
        data_dict['level'] = self.level
        data_dict['cards'] = []
        for i in self.allowed_mats:
            data_dict['cards'].append({
                'title': self.mat_text[i],
                'txt': self.calc_data[i],
                'img': self.mat_img[i],
                'card_bg': self.card_bg[i]
            })
        
        for i in ['xp_wasted', 'xp_req']:

            data_dict[i] = self.calc_data[i]
        
        if 'mora' in self.calc_data:
                data_dict['cards'].append({
                'title': 'Mora',
                'txt': self.calc_data['mora'] if 'mora' in self.calc_data else 0,
                'img': self.mat_img['mora'],
                'card_bg': self.card_bg['mora']
            })
        
        return data_dict













