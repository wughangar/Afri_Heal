#!/usr/bin/python3
"""
Patient model
"""

from sqlalchemy import Column, String, Integer
from models.base_model import BaseModel


class Patient(BaseModel):
    user_id = Column(String(60), nullable=True)
    history = Column(String(1024), nullable=False)


    def __init__(self, *args, **kwargs):
        """initializes Patient"""
        super().__init__(*args, **kwargs)