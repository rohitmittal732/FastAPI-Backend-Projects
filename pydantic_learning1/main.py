from fastapi import FastAPI,Body
from typing import Optional
from enum import Enum
from pydantic import BaseModel
from random import randrange

app=FastAPI()

class Lights(str,Enum):
   green = "go"
   yellow = "wait"
   red = "stop"
    
@app.get("/color/{color}")
def light(color:Lights):
    return {"message":color.value}

class Posts(BaseModel):
    title:str
    content:str
    published:bool=True
    rating:Optional[int]=None
    
my_post=[{"title":"typing","content":"typing fast to make type","rating":4},
         {"title":"reading","content":"atomic habits book read by rohit","rating":5}]

from enum import Enum

from fastapi import FastAPI


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

@app.get("/hello")
def hello():
    return {"message":"hello"}

@app.get("/home")
def home():
    return {"message":"this is homepage"}

@app.get("/about")
def about():
    return {"message":"this is about page"}

@app.get("/items")
def items():
    return {"menu":"dosa,burger,cheese cake,french fries"}

@app.get("/items/{dosa}")
def read_item(dosa:str):
    return {"item id":dosa}

@app.get("/hello/{id}")
def hello(id: int):
    return {"id": id}

# @app.get("/posts/{post_rating}")
# def find_post(post_rating:int):
#     for i in my_post:
#         if post_rating==my_post[0]["rating"]:
#             return i


@app.get("/users")
async def read_users():
    return ["Rick", "Morty"]


@app.get("/users")
async def read_users2():
    return ["Bean", "Elfo"]
    

# @app.post("/posts/{posts_id}")
# def posts(posts_id:int,new_post:Posts):
#     print(new_post.rating)
#     return {"post_id":posts_id,"title":new_post.title}

@app.get("/posts")
def all_post(post:Posts):
    new_post=post.model_dump()
    return new_post
    

@app.post("/posts")
def posts(post:Posts):
    new_post=post.model_dump()
    my_post.append(new_post)
    return new_post


