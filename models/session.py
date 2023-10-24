#!/usr/bin/python3
"""
Session model
""" 
    
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel


class Session(BaseModel):
    __tablename__ = "sessions"
    category_id = Column(String(60), ForeignKey('categories.id'))
    therapist_id = Column(String(60))
    date = Column(DateTime)
    duration = Column(DateTime)
    status = Column(Boolean)

    category = relationship('Category', back_populates='sessions')


    def __init__(self, *args, **kwargs):
        """initializes Session"""
        super().__init__(*args, **kwargs)