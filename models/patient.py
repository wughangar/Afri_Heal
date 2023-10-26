#!/usr/bin/python3
"""
Patient model
"""

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel


class Patient(BaseModel):
    __tablename__ = "patients"
    user_id = Column(String(60), ForeignKey('users.id'), unique=True)
    history = Column(String(1024), nullable=False)

    user = relationship('User', back_populates='patient')
    bookings = relationship('Booking', back_populates='patient')


    def __init__(self, *args, **kwargs):
        """initializes Patient"""
        super().__init__(*args, **kwargs)