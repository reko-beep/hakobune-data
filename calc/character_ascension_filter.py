import typing

class CharacterAscensionFilter:
    '''
    
    Filter to parse ascension data for each talent levelup for
    a ascension
    
    '''
    
    def __init__(self, talent_data: typing.List[typing.List[dict]]):

        self.data_to_parse = talent_data
        self.dict_ = {
            '2': [ 
                {
                    'level': 2,
                    'mats': 2
                }               
                
            ],
            '3': [
                {
                    'level': 3,
                    'mats': 2
                } ,
                {
                    'level': 4,
                    'mats': 2
                } 
            ],
            '4': [
                {
                    'level': 5,
                    'mats': 2
                } ,
                {
                    'level': 6,
                    'mats': 2
                } 
            ],
            '5': [
                {
                    'level': 7,
                    'mats': 3
                } ,
                {
                    'level': 8,
                    'mats': 3
                } 
            ],
            '6': [
                {
                    'level': 9,
                    'mats': 3
                } ,
                {
                    'level': 10,
                    'mats': 4
                } 
            ]
        }



        self.__parse()


    def fix_amount(self, text: str):
            if ',' in text:
                text = text.replace(",",'',99)
            if 'N/A' in text:
                text = text.replace('N/A', '0', 99)            
            if '.' in text:
                text = int(float(text))            
            return int(text)

    def __parse(self):
        total = {}
        for ascension in self.dict_ :
    
            talent_levels = self.dict_[ascension]
            for talent in talent_levels:

                materials = int(talent['mats']) + 1 # amount of materials to get
                index = int(talent['level']) - 2 # index of mats from scraped data
                
                list_ = []

                for i in range(materials):

                    list_.append(self.data_to_parse[i][index])
                
                talent['mats'] = list_

                for it in list_:
                    if it is not None:
                        if it['title'] not in total:
                            total[it['title']] = {'txt': self.fix_amount(it['txt']), 'img': it['img'], 'card_bg': it['card_bg']}
                        else:
                            total[it['title']]['txt'] += self.fix_amount(it['txt'])  

        return_form = []

        for name in total:
            return_form.append({'title': name, 'txt': total[name]['txt'], 'img': total[name]['img'], 'card_bg': total[name]['card_bg']})
       
        self.dict_['total'] = return_form


    
    @property
    def data(self):

        return self.dict_