from flask import Flask, request
from models import db, init_db, User
from werkzeug.security import generate_password_hash
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath('instance/athlete_app.db')
init_db(app)

# Simulate the full register route
def register():
    try:
        # Simulate form data
        username = 'testuser4'
        email = 'test4@example.com'
        height = 170.0
        weight = 70.0
        password = 'testpass4'
        bio = ''

        print('Processing registration...')

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

        print('User created successfully')
        return 'success'

    except Exception as e:
        print('Error:', str(e))
        import traceback
        traceback.print_exc()
        return 'error'

with app.app_context():
    result = register()
    print('Result:', result)
