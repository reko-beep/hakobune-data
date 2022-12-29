from requests import Session
from utils import get_tables, find_image, find_rarity, find_text, find_url
from routes import ROUTES

from bs4 import BeautifulSoup


class GenshinClient:

    def __init__(self) -> None:
        self.session = Session()
        
    def get_characters_list(self):        
        src = self.session.get(ROUTES.CHARACTERS).content
        bs = BeautifulSoup(src, 'lxml')
        
        tables = [get_tables(bs, 'Playable_Characters', True)] + [get_tables(bs, 'Upcoming_Playable_Characters', True)]
        obj_dict = []
        for table in tables:
            rows = table.find_all('tr')[1:]
            for row in rows:
                cols = row.find_all('td')
                keys = ['link', 'img', 'rarity', 'name','element', 'weapon', 'nation']
                values = [find_url(cols[0]), find_image(cols[0]), find_rarity(cols[2]), find_text(cols[1]), find_text(cols[3]), find_text(cols[4]), find_text(cols[5])]
                obj_dict.append(dict(zip(keys, values)))
                
        return obj_dict
        
     
test = GenshinClient()
print(test.get_characters_list())