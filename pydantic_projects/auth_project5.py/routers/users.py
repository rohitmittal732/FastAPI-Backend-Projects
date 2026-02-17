from fastapi import APIRouter,Depends,HTTPException,status
import schemas,models,utils
from database import get_db
from sqlalchemy.orm import Session

router=APIRouter()




@router.get("/users",response_model=list[schemas.User_out])
def get_user(db:Session=Depends(get_db)):
    user_info=db.query(models.Users).all()
    return user_info

@router.post("/users",response_model=list[schemas.User_out])
def new_user(user:schemas.User_in,db:Session=Depends(get_db)):
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    user_data=models.Users(email=user.email,password=user.password)
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return [user_data]