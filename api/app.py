from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models.engine.db_config import DbConfig
from models.database import db
from models.therapist import Therapist
from models.patient import Patient
from models.afri_user import User
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Loki1994@localhost/afriheal'
db = SQLAlchemy(app)
#db.init_app(app)

Session = sessionmaker(bind=db)


@app.route('/')
def afri_web():
    return 'We are building Afri-world1'

@app.route('/api/users', methods=['GET'])
def get_users():
    """
    retrive a list of of users(Get method)
    """
    session = Session()
    users = session.query(User).all()
    user_list = [user.to_dict() for user in users]
    session.close()
    return jsonify(user_list)

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(**data)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

@app.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})

@app.route('/api/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    data = request.json
    for key, value in data.items():
        setattr(user, key, value)
    db.session.commit()
    return jsonify(user.to_dict())


if __name__ == '__main__':
    app.run()
