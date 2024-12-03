from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship
from datetime import datetime
from pydantic import EmailStr
from sqlalchemy.ext.declarative import declarative_base


class UpdatePost(SQLModel):
    title: str = Field()
    content: str = Field()
    published: bool|None = Field(default=True)


class User(SQLModel, table=True):
    id: int|None = Field(primary_key=True)
    email: EmailStr = Field(unique=True)
    password: str 
    created_at: datetime|None = Field(default_factory=datetime.now, sa_column_kwargs={"server_default": "now()"})

class UserOut(SQLModel):
    id: int
    email: EmailStr 

class Posts(SQLModel, table=True):
    id: int|None = Field(primary_key=True)
    title: str = Field()
    content: str = Field()
    published: bool|None  = Field(default=True,sa_column_kwargs={"server_default": "true"})
    created_at: datetime|None = Field(default_factory= datetime.now,sa_column_kwargs={"server_default": "now()"})
    owner_id: int = Field(foreign_key="user.id", ondelete='CASCADE')
    owner : User|None = Relationship()

class PostResponse(UpdatePost):
    id: int 
    created_at: datetime
    owner_id: int
    owner: UserOut

class PostOut(UpdatePost):
    votes: int

#https://sqlmodel.tiangolo.com/tutorial/relationship-attributes/read-relationships/
class UserCreate(SQLModel):
    email: EmailStr
    password: str

class Token(SQLModel):
    access_token: str 
    token_type: str  


class TokenData(SQLModel):
    id: str | None 
    

class Votes(SQLModel, table=True):
    user_id: int = Field(foreign_key='user.id',ondelete='CASCADE', primary_key=True)
    post_id: int = Field(foreign_key='posts.id', ondelete='CASCADE', primary_key=True)


class VoteOut(SQLModel):
    post_id: int
    up_direction: bool


Base = declarative_base()
Base.metadata = SQLModel.metadata