
from enum import Enum
from urllib.parse import urljoin

class ROUTES(str, Enum):
    MAIN = 'https://genshin-impact.fandom.com/wiki/'
    CHARACTERS = 'Character/List'
    
    
    
    def __str__(self) -> str:
        if self.value != 'https://genshin-impact.fandom.com/wiki/':
            return urljoin('https://genshin-impact.fandom.com/wiki/', self.value)
        return self.value

    def __call__(self, path: str) -> str:
        return urljoin(self.value, path)
        