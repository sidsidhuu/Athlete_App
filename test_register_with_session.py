from flask import Flask, session, request
from flask_session import Session
from models import db, init_db, User
from werkzeug.security import generate_password_hash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath('instance/athlete_app.db')
init_db(app)

Session(app)

# Simulate the full register route with session
def register():
    try:
        # Simulate form data
        username = 'testuser5'
        email = 'test5@example.com'
        height = 170.0
        weight = 70.0
        password = 'testpass5'
        bio = ''

        print('Processing registration with session...')

        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print('Username already exists')
            return 'error'

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            print('Email already exists')
            return 'error'

        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
            height=height,
            weight=weight,
            bio=bio
        )

        db.session.add(new_user)
        db.session.commit()

        # Log user in (session)
        session['user_id'] = new_user.id
        session['user'] = username

        print('User created and logged in successfully')
        print('Session user_id:', session.get('user_id'))
        print('Session user:', session.get('user'))
        return 'success'

    except Exception as e:
        print('Error:', str(e))
        import traceback
        traceback.print_exc()
        return 'error'

with app.test_request_context():
    result = register()
    print('Result:', result)
