
import string
from bs4 import BeautifulSoup, Tag, NavigableString
import typing

def generate_key(text: str):
    
    """generates a key for a dictionary

    Returns:
        str: a key
    """    
    return text.replace('_',' ',99).translate(text.maketrans('', '', string.punctuation)).replace('%20', '',99).replace('%27', '', 99).replace(' ','_',99).lower()


def between_elements(bs:BeautifulSoup , element: typing.Union[Tag, NavigableString], end_element: typing.Union[Tag, NavigableString] = None) -> list[typing.Union[Tag, NavigableString]]:
    """function returns a list of all elements between 2 elements

    Args:
        element (typing.Union[Tag, NavigableString]): an element object returned with find or find_all
        end_element (typing.Union[Tag, NavigableString]): an element object returned with find or find_all
        

    Returns:
        list[typing.Union[Tag, NavigableString]] : a list of all elements between 2 elements
    """
    elements = []
    
    if end_element is None:
        element_cursor = [e for e in element.find_next_siblings() if e.name != element.name]
    else:
        element_cursor = [e for e in element.find_next_siblings() if e == end_element]
    
    return element_cursor

def find_image(element: typing.Union[Tag, NavigableString]) -> str:
    """function returns a image found within the Tag element

    Args:
        element (typing.Union[Tag, NavigableString]): an element object returned with find or find_all
        

    Returns:
        str : image url
    """    
    
    img_url = ''
    if element.name != 'img':
        element = element.find('img')
    
    if element is not None:
        
        if 'data-src' in element.attrs:
            if element.attrs['data-src'].startswith('http'):
                img_url =  element.attrs['data-src'][:element.attrs['data-src'].find('/revision')]
        
        if img_url == '':
            if 'src' in element.attrs:
                if element.attrs['src'].startswith('http'):
                    img_url = element.attrs['src'][:element.attrs['src'].find('/revision')]
        
        return img_url
    
    return 'https://i.imgur.com/ANDxNKv.png'


def get_tables(bs: BeautifulSoup, id: str, single: bool = True) -> list[typing.Union[Tag, NavigableString]]:
    """function returns a table with specific

    Args:
        bs (BeautifulSoup): BeautifulSoup Object
        id (str): table id name

    Returns:
        list[typing.Union[Tag, NavigableString]]: list of Tag elements having name table
    """    
    
    table_adjacent = bs.find('span', {'id': id})
    if table_adjacent is not None:
        table_adjacent = table_adjacent.parent
        tables = [e for e in table_adjacent.find_next_siblings() if e.name == 'table']
        
        if single:            
            return tables[0] if len(tables) > 0 else None
        return tables
      
        
def get_datasource(self, bs: BeautifulSoup, **kwargs
                        ):
    
        
    """gets data from beautiful soup object usinng the data sources provided
    
    keyword arguments
    ---------------------
    
    datasources : list[{'div': name, 'type': 'txt_list' or 'txt', 'ds': datasource name}]

    Returns:
        dict : containing data
    """        

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


def replace_artifact(string_ : str):
    s = ['Flower of Life', 'Plume of Death', 'Sands of Eon', 'Goblet of Eonothem', 'Circlet of Logos']
    for _ in s:
        string_ = string_.replace(_, '', 1)
    return string_



def get_card_info(card_container_div: typing.Union[Tag, NavigableString]):
    
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

        img_link = find_image(img)
        second_title = card_container_div.find('div', {'class': 'card_text'}).text if card_container_div.find('div', {'class': 'card_text'}) is not None else 'N/A'
        card_bg_img = ''
        card_bg_select = list(set(list(cards_bg.keys())).intersection(card_container_div.attrs['class']))
        if len(card_bg_select) != 0:
            card_bg_img = cards_bg[card_bg_select[0]]
        
        return {
            'title': title,
            'img': img_link,
            'txt': second_title,
            'card_bg': card_bg_img,
            'rarity' : int(card_bg_select[0].replace('card_', '', 1))
        }

def find_rarity(element: typing.Union[Tag, NavigableString]) -> int:
    """function returns a rarity found within the Tag element

    Args:
        element (typing.Union[Tag, NavigableString]): an element object returned with find or find_all
        

    Returns:
        int : integer
    """    
    
    img_url = ''
    if element.name != 'img':
        element = element.find('img')
    
    if element is not None:        
    
        if 'alt' in element.attrs:
            if element.attrs['alt'][0].isdigit():
                return int(element.attrs['alt'][0])
        
        return 0
    
    return 0

def find_text(element: typing.Union[Tag, NavigableString]) -> str:
    """function returns a text within the Tag element

    Args:
        element (typing.Union[Tag, NavigableString]): an element object returned with find or find_all
        

    Returns:
        str : text
    """    
    
    
    
    if element is not None:         
        return element.text.strip()
  
    
    return 'Nothing Found'