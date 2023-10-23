#!/usr/bin/python3
"""
Review model
""" 
    
from sqlalchemy import Column, String, DateTime, Integer
from models.base_model import BaseModel


class Review(BaseModel):
    patient_id = Column(String(60))
    therapist_id = Column(String(60))
    rating = Column(Integer)
    date = Column(DateTime)
    comments = Column(String(1024))

    def __init__(self, *args, **kwargs):
        """initializes Review"""
        super().__init__(*args, **kwargs)