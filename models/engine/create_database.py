from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base_model import BaseModel
from models.user import User
from models.therapist import Therapist
from models.review import Review

database_url = 'mysql://root:Loki1994@localhost/afriheal'

engine = create_engine(database_url)
Session = sessionmaker(bind=engine)
session = Session()

BaseModel.metadata.create_all(engine)

session.close()
