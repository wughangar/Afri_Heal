#!/usr/bin/python3
"""
base model declaration
"""

import uuid
import os
import sys
from models import storage
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

time = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel:
    """
    constain methods and atributes to be inherited by other models 
    """
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """
        Initialize the base model
        """
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
                if kwargs.get("created_at", None) and type(self.created_at) is str:
                    self.created_at = datetime.strptime(kwargs["created_at"], time)
                else:
                    self.created_at = datetime.utcnow()
                if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                    self.updated_at = datetime.strptime(kwargs["updated_at"], time)
                else:
                    self.updated_at = datetime.utcnow()
                if kwargs.get("id", None) is None:
                    self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at
    

    def __str__(self):
        """
        String representation of the base class
        defines a human-readable and informative string representation
        useful for debugging, logging, and providing meaningful output 
        when used in contexts like printing or string formatting
        """
        return"[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id, self.__dict__)
    

    def __dict__(self, save_fs=None):
        """
        convert an instance of a class into a dictionary representation
        allows objects to be easily converted into a format suitable for purposes like:
        storage, transmission and ensuring security
        """
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        new_dict["__class__"] = self.__class__.__name__

        # Remove sqlachemy key, not needed for serialization 
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]

        # Remove password before serialization to ensure security
        if save_fs is None:
            if "password" in new_dict:
                del new_dict["password"]
        return new_dict
    

    def save(self):
        """
        update 'updated_at' with current time
        call storage new method to ...
        call storage save to ...
        """
        self.updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()


    def delete(self):
        """
        delete current instance from  db
        """
        storage.delete(self)

