#!/usr/bin/python3
"""
datatabase configuration
"""

from models.afri_user import User
from models.patient import Patient
from models.therapist import Therapist
from models.booking import Booking
from models.session import Session
from models.category import Category
from models.review import Review
from models.payment import Payment
from models.base_model import BaseModel, Base

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {
    "User": User, "Patient": Patient, "Therapist": Therapist, "Booking": Booking,
    "Session": Session, "Category": Category, "Review": Review, "Payment": Payment
}

class DbConfig:
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine('mysql+mysqldb://root:SaisaRoot@localhost/afriheal')

    def all(self, cls=None):
        """
        query the current db session
        """
        new_dict = {}
        for i in classes:
            if cls is None or cls is classes[i] or cls is i:
                objs = self.__session.query(classes[i]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return new_dict
    

    def new(self, obj):
        """
        add object to the current session
        """
        self.__session.add(obj)

    def save(self):
        """
        commit the changes to  current db session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        delete from current db session
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session

    def close(self):
        self.__session.remove()

    def get(self, cls, id):
        from models import storage
        """
        Returns the object bsed on the class name and its id
        returns None id not found
        """
        if cls not in classes.values():
            return None
        
        all_classes = storage.all(cls)
        for value in all_classes.values():
            if value.id == id:
                return value
        return None
    
    def count(self, cls=None):
        from models import storage
        """
        count the number of objects in the db
        """
        all_classes = classes.values()

        if not cls:
            count = 0
            for clss in all_classes:
                count += len(storage.all(clss).values())
        else:
            count = len(storage.all(cls).values())
        return count