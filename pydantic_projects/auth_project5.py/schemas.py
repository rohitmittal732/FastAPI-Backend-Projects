from pydantic import BaseModel,EmailStr,SecretStr
from datetime import datetime
from typing import Optional

class Post(BaseModel):
    title:str
    content:str
    published:Optional[bool]=True
    id:Optional[int|None]=None

class PostCreate(Post):
    pass

class PostOut(Post):
    id:int
    created_at:datetime
    owner_id:int
    

class User_in(BaseModel):
    email:EmailStr
    password:str
    
class User_out(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    
    class Config:
        from_attributes=True
        
class Token(BaseModel):
    access_token:str
    token_type:str
    
class Tokendata(BaseModel):
    id:Optional[int]
