#!/usr/bin/python3
"""
Booking model
""" 
    
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel


class Booking(BaseModel):
    __tablename__ = "bookings"
    patient_id = Column(String(60), ForeignKey('patients.id'))
    therapist_id = Column(String(60), ForeignKey('therapists.id'))
    session_id = Column(String(60), ForeignKey('sessions.id'))
    date = Column(DateTime)
    status = Column(Boolean)

    patient = relationship('Patient', back_populates='bookings', foreign_keys=[patient_id])
    therapist = relationship('Therapist', back_populates='bookings', foreign_keys=[therapist_id])
    session = relationship('Session', back_populates='bookings', foreign_keys=[session_id])

    def __init__(self, *args, **kwargs):
        """initializes Booking"""
        super().__init__(*args, **kwargs)