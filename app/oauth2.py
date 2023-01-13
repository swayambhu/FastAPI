from jose import JWTError, jwt
from datetime import datetime, timedelta
from .schemas import TokenData
from .database import get_db
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .models import User
#SECRET_KEY
#ALGORITHM
#Expriation time

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "99bf8dedb7396e4a9486fc3a0c08dbc4e94d806e1ffcf9bc93f0eb9e40cfe81579d807feaf29315dd5e91ee124649f628d1f36f9ba7d43831fe2ab0b34130ed64ff40a1229d781c1bfa6bc0128ddc8549a1836db4a85e9a88ef786e299984d991d8a2322e9ab25b191855b60002e5439b793e0aebc9f972cd2665c1ebfbe36a3"

ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60

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
        
    