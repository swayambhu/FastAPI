from jose import JWTError, jwt
from datetime import datetime, timedelta
from .schemas import TokenData
from .database import get_db
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .models import User
from . import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')



SECRET_KEY = config.SECRET_KEY

ALGORITHM = config.ALGORITHM

ACCESS_TOKEN_EXPIRE_MINUTES = int(config.ACCESS_TOKEN_EXPIRE_MINUTES)

def create_access_token(data: dict):
    to_encode =  data.copy()
    expire = datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id= id)
        
    except JWTError:
        raise credentials_exception
    
    return token_data
    

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Could not validate credentials', headers={
        "WWW-Authenticate": "Bearer"
    })
    user_data = verify_access_token(token, credentials_exception)
    
    user = db.query(User).filter(User.id == user_data.id).first()
    return user
        
    