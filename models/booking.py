#!/usr/bin/python3
"""
Booking model
""" 
    
from sqlalchemy import Column, String, DateTime, Boolean
from models.base_model import BaseModel


class Booking(BaseModel):
    __tablename__ = "bookings"
    patient_id = Column(String(60))
    therapist_id = Column(String(60))
    session_id = Column(String(60))
    date = Column(DateTime)
    status = Column(Boolean)

    def __init__(self, *args, **kwargs):
        """initializes Booking"""
        super().__init__(*args, **kwargs)