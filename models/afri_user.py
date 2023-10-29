#!/usr/bin/python3
"""
User model
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel
from hashlib import md5
from models.database import db

db = SQLAlchemy()
#from models.therapist import Therapist
#from models.patient import Patient

class User(BaseModel):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    phone = Column(Integer, nullable=False, unique=True)
    email = Column(String(128),nullable=False, unique=True)
    password = Column(String(60), nullable=False)
    role = Column(String(60), nullable=False)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    therapist_id = Column(Integer, ForeignKey('therapists.id'))

    therapist = relationship('Therapist', back_populates='user', uselist=False, foreign_keys=[therapist_id])
    patient = relationship('Patient', back_populates='user', uselist=False, foreign_keys=[patient_id])

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
