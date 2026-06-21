from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)

class UserCreate(BaseModel):
    username : str
    email : str
    password : str

class UserLogin(BaseModel):
    email: str
    password : str