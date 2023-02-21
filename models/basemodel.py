#!/usr/bin/env python3
"""
    base model module
"""
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
import models

Base = declarative_base()

list_params = ["id", "__class__"]

class BaseModel:
    """
        Default model
    """
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, **kwargs) -> None:
        """ constructor function """
        if kwargs:
            for key, value in kwargs.items():
                if key == "updated_at":
                    value = datetime.utcnow()

                if key == "created_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")

                if key not in list_params:
                    setattr(self, key, value)
        if not self.id:
            self.id = str(uuid4())
        if not self.created_at:
            self.created_at = datetime.utcnow()
        if not self.updated_at:
            self.updated_at = datetime.utcnow()

    # def save(self):
    #     """updates the attribute 'updated_at' with the current datetime"""
    #     self.updated_at = datetime.utcnow()
    #     models.storage.new(self)
    #     models.storage.save()

    def to_dict(self) -> dict:
        """ to_dict method """
        new_dict = self.__dict__.copy()

        # save the string format of time
        new_dict["created_at"] = self.created_at.isoformat()
        new_dict["updated_at"] = self.updated_at.isoformat()
        new_dict["__class__"] = self.__class__.__name__
        return new_dict
