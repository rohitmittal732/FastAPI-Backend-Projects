from typing import Annotated
from pydantic import BaseModel
from fastapi import FastAPI,Path

app=FastAPI()

class Item(BaseModel):
    name:str
    description:str|None=None
    price:float
    tax:float|None=None

@app.put("/items/{item_id}")
def item(item_id:Annotated[int,Path(title="item of the id",ge=0,le=100)],q:str|None=None,item:Item|None=None):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results
    