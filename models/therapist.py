#!/usr/bin/python3
"""
Therapist model
"""

from sqlalchemy import Column, String, Boolean
from models.base_model import BaseModel


class Therapist(BaseModel):
    user_id = Column(String(60))
    specialization = Column(String(128))
    experience = Column(String(128))
    availability = Column(Boolean())

    def __init__(self, *args, **kwargs):
        """initializes Place"""
        super().__init__(*args, **kwargs)