from flask import Flask, session, request
from flask_session import Session
from models import db, init_db, User
from werkzeug.security import generate_password_hash
import os

app = Flask(__name__)
app.secret_key = 'test'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath('instance/athlete_app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Session(app)
init_db(app)

with app.test_request_context():
    # Simulate register logic
    username = 'testuser14'
    email = 'test14@example.com'
    height = 170.0
    weight = 70.0
    password = 'testpass14'
    bio = ''

    # Check if user already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        print('Username already exists')
    else:
        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
            height=height,
            weight=weight,
            bio=bio,
            profile_photo=None
        )

        db.session.add(new_user)
        db.session.commit()

        # Log user in
        session['user_id'] = new_user.id
        session['user'] = username

        print('User created successfully')
        print('Session user_id:', session.get('user_id'))
        print('Session user:', session.get('user'))
