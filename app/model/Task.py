import json
from typing import Optional
from pydantic import BaseModel

class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    done: Optional[bool] = False
    
    @classmethod
    def from_list(cls, tpl):
        return cls(**{k: v for k, v in zip(cls.model_fields.keys(), tpl)})