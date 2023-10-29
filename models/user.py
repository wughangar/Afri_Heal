#!/usr/bin/python3
"""
User model
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer
from models.base_model import BaseModel

db = SQLAlchemy()
#from models.therapist import Therapist
#from models.patient import Patient

class User(BaseModel):
    __tablename__ = "users"
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    phone = Column(Integer, nullable=False, unique=True)
    email = Column(String(128),nullable=False, unique=True)
    password = Column(String(60), nullable=False)


    def __init__(self, *args, **kwargs):
        """
        Initialize user
        """
        super().__init__(*args, **kwargs)