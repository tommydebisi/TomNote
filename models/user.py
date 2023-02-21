#!/usr/bin/python3
"""
    User module
"""
from sqlalchemy import Column, String
from models.basemodel import BaseModel, Base
from sqlalchemy.orm import relationship
from models.notes import Note

class User(BaseModel, Base):
    """ User class """
    __tablename__ = 'users'
    hashed_password = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    notes = relationship('Note', backref="user", cascade="all, delete")
