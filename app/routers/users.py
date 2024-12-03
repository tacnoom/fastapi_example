from fastapi import APIRouter,status, HTTPException
from sqlmodel import text
from .. import models 
from .. import utils
from .. import database

router = APIRouter(
    tags=['Users']
)

@router.post('/create_user', status_code=status.HTTP_201_CREATED, response_model=models.UserOut)
def create_user(user: models.UserCreate, session: database.SessionDep):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    user = models.User(**user.model_dump())

    session.add(user)
    session.commit()
    session.refresh(user)

    return user

@router.get('/users/{id}', response_model=models.UserOut)
def get_user(id:int, session:database.SessionDep):

    # query = text(f'''select * from "public".user where id={id}''')
    # user = session.exec(query).one()
    user = session.get(models.User, id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= 'user not found')

    return user