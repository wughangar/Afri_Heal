#!/usr/bin/python3
"""
Session model
""" 
    
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel


class Session(BaseModel):
    __tablename__ = "sessions"
    category_id = Column(String(60), ForeignKey('categories.id'))
    therapist_id = Column(String(60), ForeignKey('therapists.id'))
    date = Column(DateTime)
    duration = Column(Integer)

    category = relationship('Category', back_populates='sessions')
    therapist = relationship('Therapist', back_populates='sessions')
    bookings = relationship('Booking', back_populates='session')

    def __init__(self, *args, **kwargs):
        """initializes Session"""
        super().__init__(*args, **kwargs)
