from flask import Flask
from models import db, init_db, User
from werkzeug.security import generate_password_hash
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath('instance/athlete_app.db')
init_db(app)

with app.test_request_context():
    try:
        # Simulate the register route logic
        username = 'testuser3'
        email = 'test3@example.com'
        height = 170.0
        weight = 70.0
        password = 'testpass3'
        bio = ''

        print('Checking existing users...')
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print('Username already exists')
            exit(1)

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            print('Email already exists')
            exit(1)

        print('Creating new user...')
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

        print('User created successfully')

    except Exception as e:
        print('Error:', str(e))
        import traceback
        traceback.print_exc()
