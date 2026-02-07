from pydantic import BaseModel
from typing import Optional

class Post(BaseModel):
    title:str
    content:str
    published:Optional[bool]=True
    id:Optional[int|None]=None

class PostCreate(Post):
    pass