from flask import Flask, session, request, redirect, url_for
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

# Full register route copy
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        password = request.form['password']
        bio = request.form.get('bio', '')

        print('POST request to /register received')

        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print('Username already exists')
            return 'Username already exists', 400

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            print('Email already exists')
            return 'Email already exists', 400

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

        # Log user in
        session['user_id'] = new_user.id
        session['user'] = username

        print('User created and session set')
        return redirect(url_for('dashboard'))

    return 'GET request to /register'

@app.route('/dashboard')
def dashboard():
    return 'Dashboard page'

# Test the register route
with app.test_client() as client:
    try:
        print('Testing POST /register...')
        response = client.post('/register', data={
            'username': 'testuser6',
            'email': 'test6@example.com',
            'height': '170',
            'weight': '70',
            'password': 'testpass6'
        })
        print('Response status:', response.status_code)
        print('Response data:', response.get_data(as_text=True))

        # Check if redirect happened
        if response.status_code == 302:
            print('Redirect location:', response.headers.get('Location'))

    except Exception as e:
        print('Error:', str(e))
        import traceback
        traceback.print_exc()
