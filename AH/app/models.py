from app import Base, engine
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import datetime


class User(Base):
    """ Define User """

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    role = Column(String(10), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    phone_number = Column(String(128), nullable=False)
    gender = Column(String(10), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    therapist = relationship("Therapist", back_populates="user")


class Therapist(Base):
    """ Define therapist """
    __tablename__ = 'therapists'
    id = Column(Integer, primary_key=True)
    experience_in_years = Column(Integer, nullable=False)
    specialization = Column(String(120), nullable=False)
    availability = Column(String(20), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="therapist")


Base.metadata.create_all(engine)
