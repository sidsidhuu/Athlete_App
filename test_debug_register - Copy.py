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

# Full register route copy with debug prints
@app.route('/register', methods=['GET', 'POST'])
def register():
    print('Register route called, method:', request.method)
    if request.method == 'POST':
        print('POST data received:')
        print('Form data:', dict(request.form))
        print('Files:', list(request.files.keys()))

        try:
            username = request.form['username']
            email = request.form['email']
            height = float(request.form['height'])
            weight = float(request.form['weight'])
            password = request.form['password']
            bio = request.form.get('bio', '')

            print(f'Parsed data: username={username}, email={email}, height={height}, weight={weight}')

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

            print('Adding user to session...')
            db.session.add(new_user)
            print('Committing...')
            db.session.commit()
            print('User committed successfully')

            # Log user in
            session['user_id'] = new_user.id
            session['user'] = username
            print('Session set:', session.get('user_id'), session.get('user'))

            print('Redirecting to dashboard...')
            return redirect(url_for('dashboard'))

        except Exception as e:
            print('Error in register:', str(e))
            import traceback
            traceback.print_exc()
            return 'Internal Server Error', 500

    return 'GET request to /register'

@app.route('/dashboard')
def dashboard():
    return 'Dashboard page'

# Test the register route
with app.test_client() as client:
    try:
        print('Testing POST /register...')
        response = client.post('/register', data={
            'username': 'testuser8',
            'email': 'test8@example.com',
            'height': '170',
            'weight': '70',
            'password': 'testpass8'
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
