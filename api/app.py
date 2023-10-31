#!/usr/bin/python3


from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models.engine.db_config import DbConfig
#from models.database import db
from models.therapist import Therapist
from models.user import User
from models.review import Review
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import DatabaseError


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Loki1995@localhost/afriheal'
db = SQLAlchemy(app)
#db.init_app(app)

Session = sessionmaker(bind=db)


@app.route('/')
def afri_web():
    return 'We are building Afri-world1'

#doesnt not work yet
@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        with Session() as session:
            users = session.query(User).all()
            user_list = [user.__custom_dict__() for user in users]
            return jsonify(user_list)
    except DatabaseError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'An error occurred while processing your request.'}), 500

# get user by id- method not working yet
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        with Session() as session:
            user = session.query(User).filter_by(id=user_id).first()
            if user:
                return jsonify(user.__custom_dict__())
            else:
                return jsonify({'error': 'User not found'}), 404
    except DatabaseError as e:
        app.logger.error("DatabaseError: %s", e)
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        app.logger.error("An error occurred: %s", e)
        return jsonify({'error': 'An error occurred while processing your request.'}), 500
# works
@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(**data)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.__custom_dict__()), 201

# delete user
# method works
@app.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = db.session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})

#not working yet
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


# endpoints for reviews
# create review
#works
@app.route('/api/reviews', methods=['POST'])

def create_review():
    data = request.json
    new_review = Review(**data)
    db.session.add(new_review)
    db.session.commit()
    return jsonify(new_review.id), 201

#list reviews
@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    reviews = db.session.query(Review).all()
    review_list = [review.__custom_dict__() for review in reviews]
    return jsonify(review_list)

#get review
@app.route('/api/reviews/<string:review_id>', methods=['GET'])
def get_review(review_id):
    if not review:
        return jsonify({'error': 'Review not found'}), 404
    return jsonify(review.__custom_dict__())

#update review
#not sure this method is necessary
@app.route('/api/reviews/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    review = db.session.query(Review).get(review_id)
    if not review:
        return jsonify({'error': 'Review not found'}), 404
    data = request.json
    for key, value in data.items():
        setattr(review, key, value)
    db.session.commit()
    return jsonify(review.to_dict())

#delete review
#works
@app.route('/api/reviews/<string:review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = db.session.query(Review).get(review_id)
    if not review:
        return jsonify({'error': 'Review not found'}), 404
    db.session.delete(review)
    db.session.commit()
    return jsonify({'message': 'Review deleted'})

# api endpoint for therapists
# works
@app.route('/api/therapists', methods=['POST'])
def create_therapist():
    data = request.json
    new_therapist = Therapist(**data)
    db.session.add(new_therapist)
    db.session.commit()
    return jsonify(new_therapist.id), 201

# list therapists
# works
@app.route('/api/therapists', methods=['GET'])
def get_therapists():
    therapists = db.session.query(Therapist).all()
    therapist_list = [therapist.__custom_dict__() for therapist in therapists]
    return jsonify(therapist_list)

# get therapist
#works
@app.route('/api/therapists/<string:therapist_id>', methods=['GET'])
def get_therapist(therapist_id):
    therapist = db.session.query(Therapist).get(therapist_id)
    if not therapist:
        return jsonify({'error': 'Therapist not found'}), 404
    return jsonify(therapist.__custom_dict__())

# update therapist
# works
@app.route('/api/therapists/<string:therapist_id>', methods=['PUT'])
def update_therapist(therapist_id):
    therapist = db.session.query(Therapist).get(therapist_id)
    if not therapist:
        return jsonify({'error': 'Therapist not found'}), 404
    data = request.json
    for key, value in data.items():
        setattr(therapist, key, value)
    db.session.commit()
    return jsonify(therapist.to_dict())

# delete therapist
# works
@app.route('/api/therapists/<string:therapist_id>', methods=['DELETE'])
def delete_therapist(therapist_id):
    therapist = db.session.query(Therapist).get(therapist_id)
    if not therapist:
        return jsonify({'error': 'Therapist not found'}), 404
    db.session.delete(therapist)
    db.session.commit()
    return jsonify({'message': 'Therapist deleted'})

# user to get therapit email
@app.route('/api/therapists/<string:therapist_id>/email', methods=['GET'])
def get_therapist_email(therapist_id):
    therapist = db.session.query(Therapist).filter_by(id=therapist_id).first()
    if not therapist:
        return jsonify({'error': 'Therapist not found'}), 404
    return jsonify({'email': therapist.email})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
                        
    app.run(debug=True)

