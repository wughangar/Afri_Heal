from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__, static_url_path='/assets', static_folder='../web_static/assets')
app.secret_key = 'Loki@Loki'
# Configure SQLAlchemy to use MySQL
db_uri = 'mysql+mysqlconnector://LOKI:loki_pwd@localhost/AH_DB'
engine = create_engine(db_uri)
Session = sessionmaker(bind=engine)

Base = declarative_base()
