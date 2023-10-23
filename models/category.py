#!/usr/bin/python3
"""
Category model
""" 
    
from sqlalchemy import Column, String, DateTime, Boolean
from models.base_model import BaseModel


class Category(BaseModel):
    category_name = Column(String(60))
    
    def __init__(self, *args, **kwargs):
        """initializes Category"""
        super().__init__(*args, **kwargs)