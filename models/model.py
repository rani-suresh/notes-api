from sqlalchemy import Column, Integer, String
from database import Base
from pydantic import BaseModel

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    owner_id = Column(Integer)

class NoteCreate(BaseModel):
    title: str
  