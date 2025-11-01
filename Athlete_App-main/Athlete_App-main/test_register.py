from flask import Flask
from models import db, init_db, User
from werkzeug.security import generate_password_hash
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath('instance/athlete_app.db')
init_db(app)

with app.app_context():
    try:
        # Check if user exists
        existing_user = User.query.filter_by(username='testuser').first()
        if existing_user:
            print('User already exists')
        else:
            # Create test user
            hashed_password = generate_password_hash('testpass')
            new_user = User(
                username='testuser',
                email='test@example.com',
                password=hashed_password,
                height=170.0,
                weight=70.0,
                bio='Test user',
                profile_photo=None
            )
            db.session.add(new_user)
            db.session.commit()
            print('User created successfully')

        # Verify user was created
        user = User.query.filter_by(username='testuser').first()
        print('Created user:', user.username if user else 'None')

    except Exception as e:
        print('Error:', e)
        import traceback
        traceback.print_exc()
