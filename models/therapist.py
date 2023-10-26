#!/usr/bin/python3
"""
Therapist model
"""

from sqlalchemy import Column, String, Boolean, ForeignKey
from models.base_model import BaseModel
from models.afri_user import User
from sqlalchemy.orm import relationship


class Therapist(BaseModel):
    __tablename__ = "therapists"
    user_id = Column(String(60), ForeignKey('users.id'), unique=True)
    specialization = Column(String(128), nullable=False)
    experience = Column(String(128), nullable=False)
    availability = Column(Boolean(), nullable=False, default=True)

    user = relationship('User', back_populates='therapist')
    sessions = relationship('Session', back_populates='therapist')
    bookings = relationship('Booking', back_populates='therapist')


    def __init__(self, *args, **kwargs):
        """initializes Place"""
        super().__init__(*args, **kwargs)