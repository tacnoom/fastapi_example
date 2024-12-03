from fastapi import Body, FastAPI
from pydantic import BaseModel
from psycopg.rows import dict_row
import time
import pandas as pd
from sqlalchemy.orm import Session
from . import models
from typing import Annotated, List

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, select, insert
from datetime import datetime
from .database import engine
from . import utils
from .routers import posts, users, auth, votes
from . import database
from fastapi.middleware.cors import CORSMiddleware

'''
documentation at https://fastapi.tiangolo.com/tutorial/sql-databases/?h=sql#create-models
'''
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/sqlalchemy')
def createtables(session :database.SessionDep):
    create_db_and_tables()
    return {'status': 'success'}

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

@app.get('/')
def root():
    return {'message': 'hello world'}



app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)