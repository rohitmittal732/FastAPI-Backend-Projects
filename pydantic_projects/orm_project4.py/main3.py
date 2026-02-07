from fastapi import FastAPI,status,HTTPException,status,Depends
import schemas
import models
from sqlalchemy.orm import Session
from database import engine,get_db

models.Base.metadata.create_all(bind=engine)

app=FastAPI()



@app.get("/posts")
def get_posts(db:Session=Depends(get_db)):
    posts=db.query(models.Post).all()
    return {"data":posts}

@app.get("/sqlalchemy")
def test_posts(db:Session=Depends(get_db)):
    return {"status":"success"}

@app.get("/posts/{post_id}")
def get_posts_id(post_id:int,post:schemas.Post,db:Session=Depends(get_db)):
    new_post=db.query(models.Post).filter(models.Post.id==post_id).first()
    if new_post is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f"post with {post_id} not found")
    else:
        return {"data":new_post}
    
@app.post("/posts")
def create_posts(post:schemas.PostCreate,db:Session=Depends(get_db)):
    
    new_post=models.Post(title=post.title,content=post.content,published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data":new_post}

@app.put("/posts/{post_id}")
def updated_post(post_id:int,post:schemas.Post,db:Session=Depends(get_db)):
   new_post=db.query(models.Post).filter(models.Post.id==post_id).first()

   db.add(new_post)
   db.commit()
   db.refresh(new_post)
   if new_post is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f"post is not found of index:{post_id}")
   else:
       new_post.title=post.title
       new_post.content=post.content
       new_post.published=post.published
       
       db.commit()
       db.refresh(new_post)
       return {"data":new_post}
        
    
@app.delete("/posts/{post_id}")
def deleted_post(post_id:int,post:schemas.Post,db:Session=Depends(get_db)):
    deleted_post=db.query(models.Post).filter(models.Post.id==post_id).first()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"your id:{post_id} is not in database")
    else:
        db.delete(deleted_post)
        db.commit()
        return {"message":"post deleted successfully"}