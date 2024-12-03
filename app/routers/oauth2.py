import jwt
from datetime import datetime, timedelta, timezone
from .. import models
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from ..database import SessionDep, get_session
from sqlmodel import select
from ..config import settings

'''
tokens need

secret_key
algorithm
expiration time
'''

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data:dict):
    to_encode =data.copy()
    expires = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expires})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id_str : str = payload.get("user_id")
        # print('##################################################', id_str)
        if id_str is None:
            raise credentials_exception
        
        token_data = id_str
    except jwt.PyJWTError:
        raise credentials_exception
    
    return token_data
    

def get_current_user(session: SessionDep,token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "could not authenticate", headers={'WWW-Authenticate': "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = session.exec(select(models.User).where(models.User.id ==token)).one()
    return user