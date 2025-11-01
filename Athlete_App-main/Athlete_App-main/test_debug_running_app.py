import logging
import sys

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Import and run app with debug
from flask import Flask, session, request, redirect, url_for, render_template
from flask_session import Session
from models import db, init_db, User
from werkzeug.security import generate_password_hash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath('instance/athlete_app.db')
app.config['DEBUG'] = True
init_db(app)

Session(app)

# Full register route copy with extensive debug
@app.route('/register', methods=['GET', 'POST'])
def register():
    print('=== REGISTER ROUTE CALLED ===')
    print('Method:', request.method)
    print('Headers:', dict(request.headers))
    print('Form data:', dict(request.form))
    print('Files:', list(request.files.keys()))

    if request.method == 'POST':
        try:
            print('Processing POST request...')

            username = request.form.get('username')
            email = request.form.get('email')
            height_str = request.form.get('height')
            weight_str = request.form.get('weight')
            password = request.form.get('password')
            bio = request.form.get('bio', '')

            print(f'Raw form values: username={username}, email={email}, height={height_str}, weight={weight_str}, password={"*"*len(password) if password else None}')

            # Validate required fields
            if not all([username, email, height_str, weight_str, password]):
                print('Missing required fields')
                return 'Missing required fields', 400

            height = float(height_str)
            weight = float(weight_str)

            print(f'Parsed values: height={height}, weight={weight}')

            # Check if user already exists
            print('Checking for existing user...')
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                print('Username already exists')
                return render_template('register.html', error='Username already exists')

            existing_email = User.query.filter_by(email=email).first()
            if existing_email:
                print('Email already exists')
                return render_template('register.html', error='Email already exists')

            print('Creating new user...')
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

            print('Adding to database...')
            db.session.add(new_user)
            print('Committing...')
            db.session.commit()
            print('User created successfully, ID:', new_user.id)

            # Log user in
            print('Setting session...')
            session['user_id'] = new_user.id
            session['user'] = username
            print('Session set:', session.get('user_id'), session.get('user'))

            print('Redirecting to dashboard...')
            return redirect(url_for('dashboard'))

        except ValueError as e:
            print('ValueError:', str(e))
            return 'Invalid data format', 400
        except Exception as e:
            print('Unexpected error:', str(e))
            import traceback
            traceback.print_exc()
            return 'Internal Server Error', 500

    print('Rendering register template...')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return 'Dashboard page'

if __name__ == '__main__':
    print('Starting debug app...')
    app.run(host='0.0.0.0', port=5000, debug=True)
