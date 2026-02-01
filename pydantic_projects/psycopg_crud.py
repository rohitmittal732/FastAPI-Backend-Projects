from fastapi import FastAPI,status,HTTPException
from dotenv import load_dotenv
import os
from typing import Optional
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app=FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published:Optional[bool]=True
    id:Optional[int|None]=None

load_dotenv()

    
try:
    conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    cursor_factory=RealDictCursor
)

    cursor=conn.cursor()
    print("Database connection is successfull")
except Exception as error:
    print("Database connection was successfull")
    print("error",error)
        

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts=cursor.fetchall()
    print(posts)
    return {"data":posts}

@app.get("/posts/{post_id}")
def get_posts(post_id:int):
    cursor.execute("SELECT * FROM posts WHERE id=%s ",(post_id,))
    post=cursor.fetchone()
    if post is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f"post with {post_id} not found")
    else:
        return post
    
@app.post("/posts")
def create_posts(post:Post):
    cursor.execute("""INSERT INTO posts (title,content,published) VALUES(%s,%s,%s) RETURNING *""",
                   (post.title,post.content,post.published))
    new_post=cursor.fetchone()
    conn.commit()
    return {"data":new_post}

@app.put("/posts/{post_id}")
def updated_post(post_id:int,post:Post):
   cursor.execute("UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING *",(post.title,post.content,post.published,post_id))
   updated_post=cursor.fetchone()
   conn.commit()
   if updated_post is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f"post is not found of index:{post_id}")
   else:
       return updated_post
        
    
@app.delete("/posts/{post_id}")
def deleted_post(post_id:int):
    cursor.execute("Delete From posts Where id=%s Returning *",(post_id,))
    deleted_post=cursor.fetchone()
    conn.commit()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"your id:{post_id} is not in database")
    else:
       return {"message":"post deleted successfully"}