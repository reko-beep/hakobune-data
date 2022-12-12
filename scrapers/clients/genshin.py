from requests_cache import CachedSession
from scrapers.clients.constants import GenshinRoutes
from bs4 import BeautifulSoup, NavigableString, Tag
from utils import URL
import typing

from scrapers.genshin.character import CharacterScraper

class GenshinMain:
    
    def __init__(self, client) -> None:
        from main import DataClient
        self.characters : list[CharacterScraper] = []
        self.client : DataClient = client
        self._session = self.client._session
    
    def __bsobject(self, url: URL) -> BeautifulSoup:
        with self._session.get(url) as f:
            if f.ok:
                
                return BeautifulSoup(f.content, 'lxml')
                
        
    
    def __table(self, bs : BeautifulSoup, id: str) -> typing.Union[Tag, NavigableString]:
        """
        Returns a table with specific id if it exists on the page

        Args:
            bs (BeautifulSoup): BeautifulSoup object
            id (str): string [id of the table]

        Returns:
            typing.Union[Tag, NavigableString]: 
        """        
        
        element = bs.find('span', {'id': id})
        if element is not None:
            table = [t for t in element.parent.find_next_siblings() if t.name == 'table']
            if len(table) != 0:
                return table[0]
    
    def __image(self, element: typing.Union[Tag, NavigableString]) -> str:
        if element.name != 'img':
            element = element.find('img')

        if element is not None:

            link = element.attrs['src'] if element.attrs.get('src','').startswith('http') else element.get('data-src', '')

            if link.startswith('http'):
                return link[:link.find('/revision')]
        
        return 'https://upload-os-bbs.hoyolab.com/upload/2021/09/24/38415252/f83c7d4b3a8aa199109d2e20cf52e4b9_5912579906932239478.png' 
    
    def __route(self, root: str, path: str) -> URL:
        """
        Creates a route from root path and path

        Returns:
            URL : a url object
        """        
        
        return URL(root, path)
    
    def get_characters(self):
        
        if len(self.characters) == 0:
            bs = self.__bsobject(self.__route(GenshinRoutes.MAIN, GenshinRoutes.CHARACTERS))
            table = self.__table(bs, 'Playable_Characters')
            
       
            
            if table is not None:
                keys = [t.text.replace(' ', '_', 99).strip().lower() for t in table.find('tr').find_all('th')]                                                          
                for row in table.find_all('tr')[1:]:
                    
                    cols = row.find_all('td')
                    
                    icon = self.__image(cols[0])
                    link = URL(GenshinRoutes.MAIN, cols[1].find('a').attrs['href'].replace('/wiki/', '', 1))
                    name = cols[1].text.strip()
                    rarity = int(cols[2].find('img').attrs['alt'][0]) if cols[2].find('img') is not None else 0
                    element = cols[3].text.strip()
                    weapon = cols[4].text.strip()
                    region = cols[5].text.strip()
                    gender = cols[6].text.split(' ')[-1].lower()
                    
                    data = dict(zip(keys, [icon, name, rarity, element, weapon, region, gender]))                   
                    self.characters.append(CharacterScraper(self.client, link, **data))
                    
                    
        return self.characters
                                                                                  
    
    
    
        
        
    
    
    
    