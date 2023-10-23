#!/usr/bin/python3
"""
Payment model
""" 
    
from sqlalchemy import Column, String, DateTime, Boolean, Float
from models.base_model import BaseModel


class Payment(BaseModel):
    patient_id = Column(String(60))
    therapist_id = Column(String(60))
    session_id = Column(String(60))
    amount = Column(Float)
    date = Column(DateTime)
    status = Column(Boolean)

    def __init__(self, *args, **kwargs):
        """initializes Payment"""
        super().__init__(*args, **kwargs)