from fastapi import FastAPI,status,HTTPException
from pydantic import BaseModel

app=FastAPI()

class Post(BaseModel):
    title:str
    paragraph:str
    id:int
    
myPosts=[{"title":"coding","paragraph":"coding is the best thing for skill","id":1},
        {"title":"playing chess","paragraph":"chess is the best game by which mind sharp","id":2},
        {"title":"reading books","paragraph":"reading books give knowledge","id":3}]

def find_posts(post_id:int):
    for posts in myPosts:
        if post_id==posts["id"]:
            return posts
        
def index_posts(post_id:int):
    for i in range(len(myPosts)):
        if myPosts[i]["id"]==post_id:
            return i
    return None
        

@app.get("/posts")
def get_posts():
    return myPosts

@app.get("/posts/{post_id}")
def get_posts(post_id:int):
    post=find_posts(post_id)
    if post is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f"post with {post_id} not found")
    else:
        return post
    
@app.post("/posts")
def create_posts(post:Post):
    data=post.model_dump()
    myPosts.append(data)
    return {"message":f"new post is created:{data}"}

@app.put("/posts/{post_id}")
def updated_post(post_id:int,post_:Post):
    data=post_.model_dump()
    post=index_posts(post_id)
    if post is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f"post is not found of index:{post_id}")
    else:
        data['id']=post_id
        myPosts[post].update(data)
        return myPosts[post]
    
@app.delete("/posts/{post_id}",status_code=status.HTTP_204_NO_CONTENT)
def deleted_post(post_id:int):
    index=index_posts(post_id)
    if index is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f"post is not found of index:{post_id}")
    else:
        myPosts.pop(index)
        return {"message":"post deleted successfully"}