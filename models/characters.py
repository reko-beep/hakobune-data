
from dataclasses import fields, field, dataclass

@dataclass
class Character:
    
    name : str = field(default='')
    nation: str = field(default='')
    
    
    @classmethod
    def from_dict(cls, dict_: dict):
        class_fields = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in dict_.items() if k in class_fields})