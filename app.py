from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from utils.performance import calculate_performance
import base64
import time
import subprocess
import threading
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Load model
try:
    model = load_model('models/activity_model.h5')
except Exception as e:
    print(f"Model loading failed: {e}. Using dummy predictions.")
    model = None

# Class names
classes = ['running', 'walking', 'squats', 'pushups', 'jumping_jacks', 'stretching']

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Create database tables
with app.app_context():
    db.create_all()

# Global variables for performance tracking
start_time = time.time()
activity_duration = 0

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('auth.html', error='Invalid credentials')
    return render_template('auth.html')

@app.route('/auth')
def auth():
    return render_template('auth.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        password = request.form['password']

        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()

        if existing_user:
            return render_template('register.html', error='Username already exists')
        if existing_email:
            return render_template('register.html', error='Email already exists')

        # Create new user
        new_user = User(username=username, email=email, height=height, weight=weight)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        session['user'] = username
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/settings')
def settings():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('settings.html')

@app.route('/recognition')
def recognition():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('recognition.html')

@app.route('/athlete_fitness')
def athlete_fitness():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('athlete_fitness.html')

@app.route('/gaming')
def gaming():
    if 'user' not in session:
        return redirect(url_for('login'))
    # Placeholder for gaming page
    return render_template('gaming.html')  # Assuming we'll create this later

@app.route('/challenges')
def challenges():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('challenges.html')

@app.route('/start_main_py', methods=['POST'])
def start_main_py():
    if 'user' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    try:
        # Run main.py in a separate thread to avoid blocking
        threading.Thread(target=lambda: subprocess.run(['python', 'main.py'])).start()
        return jsonify({'message': 'Main.py started'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('welcome'))

@app.route('/predict', methods=['POST'])
def predict():
    global activity_duration
    data = request.get_json()
    image_data = data['image']
    selected_activities = data.get('selected_activities', classes)  # Default to all if not specified
    # Decode base64 image
    image_data = image_data.split(',')[1]
    image_bytes = base64.b64decode(image_data)
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # Preprocess frame
    img = cv2.resize(img, (64,64))
    img = img.astype('float') / 255.0
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)

    # Predict activity
    if model:
        prediction = model.predict(img)
        predicted_class = classes[np.argmax(prediction)]
        # Filter prediction to selected activities
        if predicted_class in selected_activities:
            activity = predicted_class
        else:
            # If not in selected, pick the highest among selected or default
            selected_predictions = [prediction[0][classes.index(act)] for act in selected_activities if act in classes]
            if selected_predictions:
                activity = selected_activities[np.argmax(selected_predictions)]
            else:
                activity = predicted_class
    else:
        # Dummy prediction for demo, cycle through selected
        selected_indices = [classes.index(act) for act in selected_activities if act in classes]
        if selected_indices:
            activity = classes[selected_indices[activity_duration % len(selected_indices)]]
        else:
            activity = classes[activity_duration % len(classes)]

    # Calculate duration for performance scoring
    current_time = time.time()
    activity_duration += 1  # increment per prediction

    # Performance score
    score = calculate_performance(activity, duration_sec=activity_duration)

    return jsonify({'activity': activity, 'score': score})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
