#!/usr/bin/python3
"""
Patient model
"""

from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from models.base_model import BaseModel
from models.afri_user import User

class Patient(BaseModel):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    history = Column(String(1024), nullable=False)

    user = relationship('User', back_populates='patient')
    bookings = relationship('Booking', back_populates='patient')


    def __init__(self, *args, **kwargs):
        """initializes Patient"""
        super().__init__(*args, **kwargs)
