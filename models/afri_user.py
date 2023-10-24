#!/usr/bin/python3
"""
User model
"""

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from models.base_model import BaseModel
from hashlib import md5


class User(BaseModel):
    __tablename__ = "users"
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    phone = Column(Integer, nullable=False, unique=True)
    email = Column(String(128),nullable=False, unique=True)
    password = Column(String(60), nullable=False)
    role = Column(String(60), nullable=False)

    therapist = relationship('Therapist',uselist=False, back_populates='user')
    patient = relationship('Patient', uselist=False, back_populates='user')


    def __init__(self, *args, **kwargs):
        """
        Initialize user
        """
        super().__init__(*args, **kwargs)
        if 'password' in kwargs:
            self.password = md5(kwargs['password'].encode()).hexdigest()

    # def __init__(self, *args, **kwargs):
    #     """
    #     initialize user
    #     """
    #     super().__init__(*args, **kwargs)

    # def __setattr__(self, name, value):
    #     """
    #     sets a password with md5 encyption
    #     """
    #     if name == "password":
    #         value = md5(value.encode()).hexdigest()
    #     super().__setattr__(name, value)