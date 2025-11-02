from flask import Flask
from models import db, init_db, User
from werkzeug.security import generate_password_hash
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath('instance/athlete_app.db')
init_db(app)

with app.app_context():
    try:
        # Check existing users
        print('Existing users:', User.query.count())

        # Try to create a new user
        username = 'testuser2'
        email = 'test2@example.com'
        password = 'testpass2'
        height = 170.0
        weight = 70.0

        # Check if user exists
        existing = User.query.filter_by(username=username).first()
        if existing:
            print('User already exists')
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(
                username=username,
                email=email,
                password=hashed_password,
                height=height,
                weight=weight
            )
            db.session.add(new_user)
            db.session.commit()
            print('User created successfully')

        print('Final user count:', User.query.count())

    except Exception as e:
        print('Error:', str(e))
        import traceback
        traceback.print_exc()
