from fastapi import APIRouter, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models
from ..database import SessionDep, Depends, Annotated
from ..utils import hash, verify
from sqlmodel import select
from . import oauth2


router = APIRouter()


@router.post('/login', response_model=models.Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],session: SessionDep):
    print(form_data.username, '############################')

    user = session.exec(select(models.User).where(models.User.email ==form_data.username)).one()
 
    
    if not verify(form_data.password, user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= 'Invalid Credentials')
    if not user:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= 'Invalid Credentials')
    

    access_token = oauth2.create_access_token(data={'user_id': user.id})
    
    return {"access_token": access_token, 'token_type': 'bearer'}
