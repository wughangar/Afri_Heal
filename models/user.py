from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define your SQLAlchemy base and User model
Base = declarative_base()

class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    phone = Column(Integer, nullable=False, unique=True)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(60), nullable=False)

    def __init__(self, first_name, last_name, phone, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.password = password

    def __custom_dict__(self):
        return {
                'id' : self.id,
                'first_name' : self.first_name,
                'last_name': self.last_name,
                'phone': self.phone,
                'email': self.email,
                }
# Configure your database connection URL
DB_URL = 'mysql://root:Loki1994@localhost/afriheal'

# Create the database engine
engine = create_engine(DB_URL)

# Create the "users" table in the database
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Commit and close the session
session.commit()
session.close()
