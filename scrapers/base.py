from os import mkdir
from os.path import exists

import string
import typing


from bs4 import BeautifulSoup, Tag, NavigableString
from json import dump, load
from utils import URL, logc



class BaseScraper:
    '''
    
    Base scraper class
    
    '''

    def __init__(self, client, url: URL) -> None:
        self.url = url
        self.key = self.generate_id(self.url.path)
        self.data = {

        }    
        self.type = 'misc'
        from main import DataClient
        self.client : DataClient = client
        
   
    @property
    def name(self):

        if self.data.get('name', None) != None:
            return self.data['name']
        else:
            if self.type == 'banners':
                return ''.join([i for i in self.generate_id(self.url.path).replace("_",' ',99).title().replace("27", '', 99).replace('22', '', 99) if not i.isdigit()])
            return self.generate_id(self.url.path).replace("_",' ',99).title().replace("27", '', 99).replace('22', '', 99)

    
    def fetch(self, force: bool = False):
        '''
        fetches data from fandom
        if its been already saved in a file, loads it

        params
        ------

        force: forces the client to fetch data from fandom
        '''

        if force:
            self._scrape()
        
        else:

            raise NotImplementedError
    
    def _scrape(self):
        
        '''
        scraping script for different page here
        
        '''
        raise NotImplementedError



    def generate_id(self, string_ : str):

        '''
        
        generates id for item for comparison
        
        '''

        return string_.replace('_',' ',99).translate(string_.maketrans('', '', string.punctuation)).replace('%20', '',99).replace('%27', '', 99).replace(' ','_',99).lower()


    def __repr__(self):
        dict_ = ' '.join([f'{k}={self.__dict__[k]}' for k in self.__dict__])
        return f'<{self.__class__.__name__} {dict_}>'

    def __str__(self):

        if self.data.get('name', None) != None:
            return self.data['name']
        else:
            return self.generate_id(self.url.path).replace('_', ' ', 99).title().replace('22', '', 99).replace('27','',99)


           

    def get_datasource(self, bs: BeautifulSoup, **kwargs
                        ):
        
        '''
        gets data from specified data source in type [type_data]
        
        '''

        data_dict_ = {

        }

        def filter_list(given_list: list):

            list_ = []
            for l in given_list:
                
                if not l.replace('[','',1).replace(']','',1).isdigit():
                    if 'chapter' not in l.lower():
                        if 'constellation' not in l.lower():
                            list_.append(l)
                            
                
            return list_[0] if len(list_) == 1 else list_

        ds = kwargs.get('datasources', [])

        for d in ds:

            division_name = d.get('div', 'div')
            data_source_name = d['ds']
            type_data = d.get('type', 'txt')

            data_dict_[data_source_name] = 'N/A'

            element = bs.find(division_name, {'data-source': data_source_name})
            if element is not None:

                if data_source_name == 'rarity':
                    rarity = element.find('img')
                    if rarity is not None:
                        if rarity.attrs['alt'][0].isdigit():
                            data_dict_[data_source_name] =  '⭐' * int(rarity.attrs['alt'][0])

                
                else:

                    if data_source_name == 'image':
                        lister = {}
                        imgs = element.find_all('figure')

                        for img in imgs:

                            img_link = self.find_image(img)
                            lister[img_link.split('/')[-1].split('.')[0].split('_')[-1].lower().replace(' ','_',99)] = img_link
                        
                        data_dict_[data_source_name] = lister

                    else:

                        h3 = element.find('h3')
                        replace_text = h3.text.strip() if h3 is not None else ''
                        div = element.find('div')
                        if type_data == 'txt':
                            if div is not None:
                                if len(div.find_all('li')) > 1:
                                    data_dict_[data_source_name] =  filter_list([l.text.strip() for l in div.find('li')])

                                if div is not None:
                                    print(div.text.replace(replace_text, '', 1).strip())
                                    data_dict_[data_source_name] =  self.replace_artifact(div.text.replace(replace_text, '', 1).strip())
                            else:

                                data_dict_[data_source_name] =  self.replace_artifact(element.text.replace(replace_text, '', 1).strip())

                        if type_data == 'txt_list':

                            if div is not None:
                                listers = div.find_all('a')

                                if len(listers) >= 1:

                                    data_dict_[data_source_name] =  filter_list([l.text for l in listers])
        
        return data_dict_

    def find_image(self, element: typing.Union[Tag, NavigableString]):

        if element.name != 'img':
            element = element.find('img')

        if element is not None:

            link = element.attrs['src'] if element.attrs.get('src','').startswith('http') else element.get('data-src', '')

            if link.startswith('http'):
                return link[:link.find('/revision')]
        
        return 'https://upload-os-bbs.hoyolab.com/upload/2021/09/24/38415252/f83c7d4b3a8aa199109d2e20cf52e4b9_5912579906932239478.png'

    def replace_artifact(self ,string_ : str):
        s = ['Flower of Life', 'Plume of Death', 'Sands of Eon', 'Goblet of Eonothem', 'Circlet of Logos']
        for _ in s:
            string_ = string_.replace(_, '', 1)
        return string_
    
    def get_table(self, bs: BeautifulSoup, id_: str):

        element = bs.find('span', {'id': id_})
        if element is not None:

            element = element.parent.find_next_sibling()
            while element.name != 'table':
                element = element.find_next_sibling()
            else:
                return element

    def get_card_info(self, card_container_div: typing.Union[Tag, NavigableString]):
        
        
        cards_bg = {
            'card_3': 'https://static.wikia.nocookie.net/gensin-impact/images/5/57/Rarity_3_background.png',
            'card_4': 'https://static.wikia.nocookie.net/gensin-impact/images/c/c9/Rarity_4_background.png',
            'card_5': 'https://static.wikia.nocookie.net/gensin-impact/images/e/ea/Rarity_5_background.png',
            'card_2': 'https://static.wikia.nocookie.net/gensin-impact/images/d/d4/Rarity_2_background.png',
            'card_1': 'https://static.wikia.nocookie.net/gensin-impact/images/6/69/Rarity_1_background.png',
            'card_0': 'https://static.wikia.nocookie.net/gensin-impact/images/6/69/Rarity_1_background.png'
        }

        if 'card_container' in card_container_div.attrs['class']:

            img = card_container_div.find('div', {'class': 'card_image'})
            title = img.find('a').attrs['title'] if img.find('a') is not None else 'N/A'
            
            if title == 'N/A':

                title = card_container_div.find('div', {'class': 'card_caption'}).attrs['title'] if card_container_div.find('a') is not None else 'N/A'

            img_link = self.find_image(img)
            second_title = card_container_div.find('div', {'class': 'card_text'}).text if card_container_div.find('div', {'class': 'card_text'}) is not None else 'N/A'
            card_bg_img = ''
            card_bg_select = list(set(list(cards_bg.keys())).intersection(card_container_div.attrs['class']))
            if len(card_bg_select) != 0:
                card_bg_img = cards_bg[card_bg_select[0]]
            
            return {
                'title': title,
                'img': img_link,
                'txt': second_title,
                'card_bg': card_bg_img
            }
    
    def between_elements(self, first_element : typing.Union[Tag, NavigableString], second_element : typing.Union[Tag, NavigableString] = None):

        '''
        return all elements between two elements
        '''

        elements = []
        element = first_element.find_next_sibling()
        if second_element is None:

            while element.name != first_element.name:
                elements.append(element)
                element = element.find_next_sibling()
                if element is None:
                    break
            
        else:
            while element != second_element:
                elements.append(element)
                element = element.find_next_sibling()
                if element is None:
                    break
                
        
        return elements
    

   