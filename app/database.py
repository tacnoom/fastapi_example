from sqlmodel import create_engine
from typing import Annotated
from fastapi import Depends
from sqlmodel import Session
from .config import settings



sqlalchemy_database_url = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}' #dbtype://<username>:<password>@<ip-address OR hostname>/<dbname>

engine = create_engine(sqlalchemy_database_url)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

