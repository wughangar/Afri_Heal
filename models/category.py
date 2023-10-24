#!/usr/bin/python3
"""
Category model
""" 
    
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel


class Category(BaseModel):
    __tablename__ = "categories"
    category_name = Column(String(60))

    sessions = relationship('Session', back_populates='category')
    
    def __init__(self, *args, **kwargs):
        """initializes Category"""
        super().__init__(*args, **kwargs)