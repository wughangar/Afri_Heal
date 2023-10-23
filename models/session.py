#!/usr/bin/python3
"""
Session model
""" 
    
from sqlalchemy import Column, String, DateTime, Boolean
from models.base_model import BaseModel


class Session(BaseModel):
    category_id = Column(String(60))
    therapist_id = Column(String(60))
    date = Column(DateTime)
    duration = Column(DateTime)
    status = Column(Boolean)

    def __init__(self, *args, **kwargs):
        """initializes Session"""
        super().__init__(*args, **kwargs)