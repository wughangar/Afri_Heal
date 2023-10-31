#!/usr/bin/python3
"""
Therapist model
"""

from sqlalchemy import Column, String, Boolean, Integer
from models.base_model import BaseModel

class Therapist(BaseModel):
    __tablename__ = "therapists"
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    phone = Column(Integer, nullable=False, unique=True)
    email = Column(String(128),nullable=False, unique=True)
    password = Column(String(60), nullable=False)
    specialization = Column(String(128), nullable=False)
    experience = Column(String(128), nullable=False)
    availability = Column(String, nullable=True)

    def to_dict(self):
        return {
                'first_name': self.first_name,
                'last_name': self.last_name,
                'phone': self.phone,
                'email': self.email,
                'specialization': self.specialization,
                'experience': self.experience,
                'availability': self.availability
                }


    def __init__(self, *args, **kwargs):
        """initializes Place"""
        super().__init__(*args, **kwargs)
