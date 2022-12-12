
from enum import Enum



class GenshinRoutes(str, Enum):
    
    MAIN = 'https://genshin-impact.fandom.com/wiki/'
    CHARACTERS = 'Characters/List'
    
    def __str__(self) -> str:
        return str(self.value)
        