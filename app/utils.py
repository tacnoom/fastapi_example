from passlib.context import CryptContext
from typing import Annotated
from sqlmodel import Session
from fastapi import Depends
from sqlmodel import create_engine

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password):

    return pwd_context.hash(password)

def verify(plain_password,hashed_password):
    return  pwd_context.verify(plain_password,hashed_password)