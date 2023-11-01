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
from flask_login import LoginManager
import os
from flask import render_template, url_for, redirect, flash
from forms.registration_form import RegistrationForm
from flask_login import login_required

#from flask_mail import Mail, Message
#import sendgrid
#from sendgrid.helpers.mail import Mail, From, To, Subject, PlainTextContent, HtmlContent


app = Flask(__name__, template_folder='templates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Loki1995@localhost/afriheal'
secret_key = os.urandom(24)
app.config['SECRET_KEY'] = secret_key

db = SQLAlchemy(app)
#db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


Session = sessionmaker(bind=db)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# user profile
@app.route('/user_profile')
@login_required
def user_profile():
    # Only authenticated users can access this route
    return 'User Profile Page'

# register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# log in route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('You have been logged in!', 'success')
            return redirect(url_for('index'))  # Replace 'index' with your app's main page
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', form=form)
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
# Create a route for posting reviews
@app.route('/post_review', methods=['POST'])
def post_review():
    # Get the review data from the form submission
    rating = request.form.get('rating')
    comments = request.form.get('comments')
    therapist_id = request.form.get('therapist_id')  # Adjust this based on your form

    # Create a new review
    new_review = Review(rating=rating, comments=comments, therapist_id=therapist_id, patient_id=current_user.id)
    db.session.add(new_review)
    db.session.commit()

    return redirect(url_for('therapist_profile', therapist_id=therapist_id))

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

# list all therapists
@app.route('/therapists')
def all_therapists():
    therapists = db.session.query(Therapist).all()
    return render_template('all_therapists.html', therapists=therapists)

# display therapits profile
@app.route('/therapists/<string:therapist_id>')
def therapist_profile(therapist_id):
    therapist = db.session.query(Therapist).get(therapist_id)
    if not therapist:
        return jsonify({'error': 'Therapist not found'}), 404
    # Render a template to display the therapist's information
    return render_template('therapist_profile.html', therapist=therapist)


# search for therapit based on criteria
@app.route('/search', methods=['GET'])
def search_therapists():
    specialization = request.args.get('specialization')
    availability = request.args.get('availability')

    # Query your database based on the specialization and availability
    therapists = db.session.query(Therapist)

    if specialization:
        therapists = therapists.filter(Therapist.specialization == specialization)

    if availability:
        therapists = therapists.filter(Therapist.availability == availability)

    therapists = therapists.all()

    # Pass the filtered therapists to your template for rendering
    return render_template('search_results.html', therapists=therapists)

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

