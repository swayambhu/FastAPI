from jose import JWTError, jwt
from datetime import datetime, timedelta
#SECRET_KEY
#ALGORITHM
#Expriation time

SECRET_KEY = "99bf8dedb7396e4a9486fc3a0c08dbc4e94d806e1ffcf9bc93f0eb9e40cfe81579d807feaf29315dd5e91ee124649f628d1f36f9ba7d43831fe2ab0b34130ed64ff40a1229d781c1bfa6bc0128ddc8549a1836db4a85e9a88ef786e299984d991d8a2322e9ab25b191855b60002e5439b793e0aebc9f972cd2665c1ebfbe36a3"

ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode =  data.copy()
    expire = datetime.now() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt
    
    