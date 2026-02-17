from jose import jwt,JWTError
from datetime import datetime,timedelta
import schemas
from fastapi import status,HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')

# SECRET_KEY="Demo_Secret_key"
ALGORITHM='HS256'
ACCESS_TOKEN_EXPIRE_MINUTES=30

def create_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,ALGORITHM)
    
    return encoded_jwt

def verify(token:str,credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id:str=payload.get("user_id")
        
        if id is None:
            raise credentials_exception
        token_data=schemas.Tokendata(id=id)
        return token_data
    except JWTError:
        raise credentials_exception
    
def get_current_user(token:str=Depends(oauth2_scheme)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid credentials",
                            headers={"WWW-Authenticate":"bearer"})
    
    return verify(token,credentials_exception)
        

    