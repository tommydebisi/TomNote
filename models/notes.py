#!/usr/bin/python3
"""
    User module
"""
from sqlalchemy import Column, String, ForeignKey
from models.basemodel import BaseModel, Base


class Note(BaseModel, Base):
    """ Note class """
    __tablename__ = 'notes'
    title = Column(String(128), nullable=True, unique=True)
    content = Column(String(128), nullable=True)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=True)
    user = None
