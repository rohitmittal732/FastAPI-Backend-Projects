from fastapi import APIRouter,Depends,HTTPException,status
from typing import List
import schemas,models,oauth2
from database import get_db
from sqlalchemy.orm import Session

router=APIRouter()

@router.get("/posts",response_model=List[schemas.PostOut])
def get_posts(db:Session=Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):
    posts=db.query(models.Post).all()
    return posts

@router.get("/sqlalchemy")
def test_posts(db:Session=Depends(get_db)):
    return {"status":"success"}

@router.get("/posts/{post_id}",response_model=schemas.PostOut)
def get_posts_id(post_id:int,post:schemas.Post,db:Session=Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):
    new_post=db.query(models.Post).filter(models.Post.id==post_id).first()
    if new_post is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f"post with {post_id} not found")
    else:
        return new_post
    
@router.post("/posts",response_model=schemas.PostOut)
def create_posts(post:schemas.PostCreate,db:Session=Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):
    
    new_post=models.Post(title=post.title,content=post.content,published=post.published,owner_id=get_current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.put("/posts/{post_id}",response_model=schemas.PostOut)
def updated_post(post_id:int,post:schemas.Post,db:Session=Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):
   new_post=db.query(models.Post).filter(models.Post.id==post_id).first()

   db.add(new_post)
   db.commit()
   db.refresh(new_post)
   if new_post is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f"post is not found of index:{post_id}")
   if new_post.owner_id != oauth2.get_current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="you are the not owner of this post")
   new_post.title=post.title
   new_post.content=post.content
   new_post.published=post.published
       
   db.commit()
   db.refresh(new_post)
   return new_post
        
    
@router.delete("/posts/{post_id}")
def deleted_post(post_id:int,post:schemas.Post,db:Session=Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):
    deleted_post=db.query(models.Post).filter(models.Post.id==post_id).first()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"your id:{post_id} is not in database")
    
    if deleted_post.owner_id != oauth2.get_current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="you are the not owner of this post")
    
    db.delete(deleted_post)
    db.commit()
    return {"message":"post deleted successfully"}


