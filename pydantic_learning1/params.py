from fastapi import FastAPI,Query,Depends
from typing import Annotated,Literal,List
from typing import Optional
from pydantic import BaseModel,Field,AfterValidator

app=FastAPI()
def strip_whitespace(v: str) -> str:
    return v.strip()

class Item(BaseModel):
    name:str
    price:int
    id:Optional[int]=None
    
class FieldParams(BaseModel):
    limit: int=Field(100,gt=0,le=100)
    offset:int=Field(0,ge=0)
    order_by:Literal["created_at","updated_at"]="created_at"
    tags:List[str]=[]

@app.get("/item")
def item(filters:FieldParams=Depends(),q:Annotated[str|None,AfterValidator(strip_whitespace),Query(title="Query String",max_length=71,pattern="^[a-zA-Z@*/-]{5,10}-123$")]=None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q and filters:
        results.update({"q": q,"filters":filters})
    return results

# example-http://127.0.0.1:8000/item?limit=10&offset=2&order_by=updated_at&tags=python&tags=fastapi&q=rohit@-123
# query parameter we learn in which field,AfterValidator,regex patterns literals,limit,offset,tags,order_by

