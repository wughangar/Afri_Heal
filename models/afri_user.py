#!/usr/bin/python3
"""
User model
"""

from sqlalchemy import Column, String, Integer
from models.base_model import BaseModel
from hashlib import md5
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base(cls=BaseModel)


class User(BaseModel):
    __tablename__ = "users"
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    phone = Column(Integer, nullable=False, unique=True)
    email = Column(String(128),nullable=False, unique=True)
    password = Column(String(60), nullable=False)
    role = Column(String(60), nullable=False)

    def __init__(self, *args, **kwargs):
        """
        initialize user
        """
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """
        sets a password with md5 encyption
        """
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)