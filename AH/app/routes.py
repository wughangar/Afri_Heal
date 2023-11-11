#!/usr/bin/python3

from app import app
from app import Session
from flask import request, render_template, redirect, url_for, session
from app.models import User, Therapist
from passlib.hash import bcrypt_sha256
import uuid
from sqlalchemy.orm import joinedload
from functools import wraps

@app.route('/', methods=['GET'], strict_slashes=False)
def welcome():
    return render_template('index.html')


@app.route('/signup/', methods=['GET', 'POST'], strict_slashes=False)
def signup():
    if request.method == 'POST':
        first_name = request.form['fname']
        last_name = request.form['lname']
        date_of_birth = request.form['dob']
        phone_number = request.form['phone']
        gender = request.form['gender']
        email = request.form['email']
        role = request.form['role']
        password = request.form['password']
        password_hash = bcrypt_sha256.hash(password)
        db_session = Session()


        # Check if username exists in AH_DB
        email_exists = db_session.query(User).filter_by(email=email).first()\
            is not None

        if email_exists:
            return "Email already exists. Please choose a \
different one."

        # Create new user
        new_user = User(first_name=first_name, last_name=last_name,
                        gender=gender, phone_number=phone_number,
                        date_of_birth=date_of_birth, email=email, role=role,
                        password=password_hash)
        db_session.add(new_user)
        db_session.commit()
        db_session.close()

        return render_template('login.html')
    cache_id = uuid.uuid4()
    return render_template('signup2.html', cache_id=cache_id)


@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    error_message = None

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db_session = Session()

        # verify password
        user = db_session.query(User).filter_by(email=email).first()

        if user:
            password_hash = user.password
            if bcrypt_sha256.verify(password, password_hash):
                session['logged_in'] = True
                session['user_id'] = user.id
 #               db_session.close()
                if user.role == 'patient':
                    return redirect(url_for('home'))
                else:
                    #db_session.add(therapist)
                    therapist = db_session.query(Therapist).filter_by(
                        user_id=session['user_id']).first()
                    #db_session.add(therapist)
                    #db_session.close()
                    if not therapist:
                        return render_template('therapist_info.html')
                    else:
                        return render_template('therapist_dashboard.html', therapist=therapist)
            else:
                db_session.close()
                error_message = "Wrong username or password"

        else:
            error_message = "User does not exist"

    return render_template('login.html', error_message=error_message)


@app.route('/home', methods=['GET'], strict_slashes=False)
def home():

    if session.get('logged_in'):
        db_session = Session()
        therapists = db_session.query(Therapist).options(joinedload(Therapist.user)).all()
        db_session.close()

        return render_template('patient_dash.html', therapists=therapists)

    else:
        return redirect(url_for('login'))


@app.route('/therapist', methods=['POST'], strict_slashes=False)
def signup_stg2():
    if request.method == 'POST':
        experience_in_years = request.form['experience']
        specialization = request.form['specialization']
        availability = request.form['availability']
        user_id = session.get('user_id')

        db_session = Session()

        therapist_info = Therapist(experience_in_years=experience_in_years,
                                   specialization=specialization,
                                   availability=availability, user_id=user_id)

        db_session.add(therapist_info)
        db_session.commit()
        db_session.close()

        return render_template('therapist_dashboard.html')

@app.route('/search', methods=['GET', 'POST'], strict_slashes=False)
def search_therapists():
    if request.method == 'POST':
        specialization = request.form['specialization']
        availability = request.form['availability']
        db_session = Session()

        therapists = db_session.query(Therapist).filter(
                Therapist.specialization.ilike(f"%{specialization}%"),
                Therapist.availability.ilike(f"%{availability}%")
        ).options(joinedload(Therapist.user)).all()
        db_session.close()
        return render_template('search.html', therapists=therapists)
    return render_template('search.html', therapists=[])

def therapist_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        user_id = session['user_id']
        db_session = Session()
        user = db_session.query(User).filter_by(id=user_id).first()
        db_session.close()
        if user and user.role == 'therapist':
            return func(*args, **kwargs)
        return "You are not authorized to access this page."
    return decorated_function

@app.route('/therapist/edit_availability', methods=['GET', 'PUT'], strict_slashes=False)
#@therapist_required
def therapist_dashboard():
    if request.method == 'PUT':
        new_availability = request.form.get('availability')
        therapist_id = session.get('user_id')
#        db_session = Session()
        therapist = db_session.query(Therapist).filter_by(user_id=therapist_id).first()
#         db_session.add(therapist)
        therapist.availability = new_availability
        db_session.commit()
        db_session.close()

    therapist_id = session.get('user_id')
    db_session = Session()
    therapist = db_session.query(Therapist).filter_by(user_id=therapist_id).first()
    db_session.add(therapist)

    db_session.close()
    return render_template('therapist_dashboard.html', therapist=therapist)


# log out
@app.route('/logout', methods=['GET'], strict_slashes=False)
def logout():
    if session.get('logged_in'):
        session.clear()
    return redirect(url_for('welcome'))
