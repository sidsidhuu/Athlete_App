from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_session import Session
from flask_migrate import Migrate
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from utils.performance import calculate_performance
from models import db, init_db, User, Follow, Post, Story, Like, Comment, Notification
import os
from datetime import datetime, timedelta
import logging

def generate_performance_insights(activity_scores, selected_activities):
    """Generate performance insights based on activity scores."""
    insights = []

    if not activity_scores:
        return ["No activities performed yet. Start exercising to see your performance insights!"]

    # Calculate average score
    avg_score = sum(activity_scores.values()) / len(activity_scores)

    # Find best and worst performing activities
    if activity_scores:
        best_activity = max(activity_scores.items(), key=lambda x: x[1])
        worst_activity = min(activity_scores.items(), key=lambda x: x[1])

        insights.append(f"Your best performance was in {best_activity[0].replace('_', ' ').title()} with a score of {best_activity[1]}")
        insights.append(f"You might want to focus more on {worst_activity[0].replace('_', ' ').title()} (score: {worst_activity[1]})")

    # Overall performance feedback
    if avg_score >= 80:
        insights.append("Excellent performance! You're in great shape.")
    elif avg_score >= 60:
        insights.append("Good job! Keep up the consistent effort.")
    elif avg_score >= 40:
        insights.append("Decent performance. Try to maintain better form and consistency.")
    else:
        insights.append("Keep practicing! Focus on proper form and technique.")

    # Activity coverage
    performed_activities = len([s for s in activity_scores.values() if s > 0])
    total_selected = len(selected_activities)
    if total_selected > 0:
        coverage = (performed_activities / total_selected) * 100
        insights.append(f"You've performed {performed_activities} out of {total_selected} selected activities ({coverage:.1f}% coverage)")

    return insights
import base64
import time
import subprocess
import threading
import os
import random
import string

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_change_in_production_123456789'  # Change this in production
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath('instance/athlete_app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Email configuration (update with your SMTP settings)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'your_app_password'  # Replace with app password
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@gmail.com'  # Replace with your email

mail = Mail(app)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'profiles'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'posts'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'stories'), exist_ok=True)

Session(app)
init_db(app)
migrate = Migrate(app, db)

# Load model
try:
    model = load_model('models/activity_model.h5')
except Exception as e:
    print(f"Model loading failed: {e}. Using dummy predictions.")
    model = None

# Class names
classes = ['running', 'walking', 'squats', 'pushups', 'jumping_jacks', 'stretching']

# Global variables for performance tracking
start_time = time.time()
activity_duration = 0

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Find user by username
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user'] = username
            logger.info(f"User {username} logged in successfully. Session ID: {session.sid if hasattr(session, 'sid') else 'N/A'}")
            return redirect(url_for('dashboard'))
        else:
            logger.warning(f"Failed login attempt for username: {username}")
            return render_template('auth.html', error='Invalid username or password')

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
        if existing_user:
            logger.warning(f"Registration failed: Username {username} already exists")
            return render_template('register.html', error='Username already exists')

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            logger.warning(f"Registration failed: Email {email} already exists")
            return render_template('register.html', error='Email already exists')

        # Create new user
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

        # Log user in
        session['user_id'] = new_user.id
        session['user'] = username
        logger.info(f"User {username} registered and logged in successfully. Session ID: {session.sid if hasattr(session, 'sid') else 'N/A'}")

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

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        # For now, just flash a message since no database
        # In a real app, save to database
        return jsonify({'message': 'Settings saved successfully!'})
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

@app.route('/performance', methods=['GET', 'POST'])
def performance():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Get activity scores from the request
        activity_scores = request.get_json().get('activity_scores', {})
        selected_activities = request.get_json().get('selected_activities', [])

        # Calculate overall performance
        scores = list(activity_scores.values())
        overall_score = sum(scores) / len(scores) if scores else 0

        # Generate insights based on scores
        insights = generate_performance_insights(activity_scores, selected_activities)

        return jsonify({
            'overall_score': round(overall_score, 2),
            'activity_scores': activity_scores,
            'insights': insights
        })

    return render_template('performance.html')

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

@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))
    user = User.query.filter_by(username=session['user']).first()
    if user:
        session['email'] = user.email
        session['height'] = user.height
        session['weight'] = user.weight
        session['profile_photo'] = user.profile_photo
        session['nickname'] = user.nickname
    return render_template('profile.html', user=user)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user' not in session:
        return redirect(url_for('login'))
    user = User.query.filter_by(username=session['user']).first()
    if request.method == 'POST':
        username = request.form['username']
        nickname = request.form.get('nickname', '').strip()
        # Check if username is taken by another user
        existing_user = User.query.filter_by(username=username).first()
        if existing_user and existing_user.id != user.id:
            flash('Username already taken', 'error')
            return redirect(url_for('edit_profile'))
        # Check if nickname is taken by another user
        if nickname:
            existing_nick = User.query.filter_by(nickname=nickname).first()
            if existing_nick and existing_nick.id != user.id:
                flash('Nickname already taken', 'error')
                return redirect(url_for('edit_profile'))
        # Update user
        user.username = username
        user.nickname = nickname if nickname else None
        db.session.commit()
        session['user'] = username
        session['nickname'] = nickname
        flash('Profile updated successfully', 'success')
        return redirect(url_for('profile'))
    return render_template('edit_profile.html')

@app.route('/upload_profile_photo', methods=['POST'])
def upload_profile_photo():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401

    if 'profile_photo' not in request.files:
        return jsonify({'success': False, 'message': 'No file provided'}), 400

    file = request.files['profile_photo']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to make filename unique
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'profiles', filename)
        file.save(filepath)

        # Update user's profile photo in database
        user = User.query.filter_by(username=session['user']).first()
        if user:
            user.profile_photo = filename
            db.session.commit()
            session['profile_photo'] = filename
            return jsonify({'success': True, 'message': 'Profile photo uploaded successfully'})
        else:
            return jsonify({'success': False, 'message': 'User not found'}), 404
    else:
        return jsonify({'success': False, 'message': 'Invalid file type'}), 400

@app.route('/update_profile_photo', methods=['POST'])
def update_profile_photo():
    if 'user' not in session:
        return redirect(url_for('login'))

    if 'profile_photo' not in request.files:
        flash('No file provided', 'error')
        return redirect(url_for('edit_profile'))

    file = request.files['profile_photo']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('edit_profile'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to make filename unique
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'profiles', filename)
        file.save(filepath)

        # Update user's profile photo in database
        user = User.query.filter_by(username=session['user']).first()
        if user:
            user.profile_photo = filename
            db.session.commit()
            session['profile_photo'] = filename
            flash('Profile photo updated successfully', 'success')
        else:
            flash('User not found', 'error')
    else:
        flash('Invalid file type', 'error')

    return redirect(url_for('edit_profile'))

@app.route('/upload_story', methods=['GET', 'POST'])
def upload_story():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        content = request.form.get('content', '').strip()
        media = request.files.get('media')

        if not media or media.filename == '':
            flash('No media file selected', 'error')
            return redirect(url_for('upload_story'))

        # Determine media type
        if media.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            media_type = 'photo'
        elif media.filename.lower().endswith(('.mp4', '.avi', '.mov')):
            media_type = 'video'
        else:
            flash('Invalid file type. Only images and videos allowed.', 'error')
            return redirect(url_for('upload_story'))

        filename = secure_filename(media.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'stories', filename)
        media.save(filepath)

        # Create story
        user = User.query.filter_by(username=session['user']).first()
        new_story = Story(
            content=content,
            media_path=filename,
            media_type=media_type,
            user_id=user.id
        )
        db.session.add(new_story)
        db.session.commit()

        flash('Story uploaded successfully!', 'success')
        return redirect(url_for('profile'))

    return render_template('upload_story.html')

@app.route('/upload_post', methods=['GET', 'POST'])
def upload_post():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        content = request.form.get('content', '').strip()
        media = request.files.get('media')
        post_type = request.form.get('post_type', 'post')  # 'post' or 'reel'

        if not media or media.filename == '':
            flash('No media file selected', 'error')
            return redirect(url_for('upload_post'))

        # Determine media type
        if media.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            media_type = 'photo'
        elif media.filename.lower().endswith(('.mp4', '.avi', '.mov')):
            media_type = 'video'
        else:
            flash('Invalid file type. Only images and videos allowed.', 'error')
            return redirect(url_for('upload_post'))

        filename = secure_filename(media.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'posts', filename)
        media.save(filepath)

        # Create post
        user = User.query.filter_by(username=session['user']).first()
        new_post = Post(
            content=content,
            video_path=filename if media_type == 'video' else None,
            activity_type=post_type,  # Use activity_type to distinguish 'post' vs 'reel'
            user_id=user.id
        )
        db.session.add(new_post)
        db.session.commit()

        flash('Post uploaded successfully!', 'success')
        return redirect(url_for('profile'))

    return render_template('upload_post.html')

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            # Generate OTP
            otp = ''.join(random.choices(string.digits, k=6))
            session['reset_otp'] = otp
            session['reset_email'] = email
            session['otp_timestamp'] = time.time()

            # Send OTP email
            msg = Message('Password Reset OTP', recipients=[email])
            msg.body = f'Your OTP for password reset is: {otp}. This OTP will expire in 10 minutes.'
            try:
                mail.send(msg)
                flash('OTP sent to your email. Please check your inbox.', 'success')
                return redirect(url_for('reset_password'))
            except Exception as e:
                logger.error(f"Failed to send OTP email: {e}")
                flash('Failed to send OTP. Please try again.', 'error')
        else:
            flash('Email not found.', 'error')
    return render_template('forgot_password.html')

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if 'reset_otp' not in session or 'reset_email' not in session:
        flash('Please request a password reset first.', 'error')
        return redirect(url_for('forgot_password'))

    # Check OTP expiration (10 minutes)
    if time.time() - session.get('otp_timestamp', 0) > 600:
        session.pop('reset_otp', None)
        session.pop('reset_email', None)
        session.pop('otp_timestamp', None)
        flash('OTP has expired. Please request a new one.', 'error')
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        otp = request.form['otp']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if otp != session['reset_otp']:
            flash('Invalid OTP.', 'error')
            return render_template('reset_password.html')

        if new_password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('reset_password.html')

        # Update password
        user = User.query.filter_by(email=session['reset_email']).first()
        if user:
            user.password = generate_password_hash(new_password)
            db.session.commit()
            session.pop('reset_otp', None)
            session.pop('reset_email', None)
            session.pop('otp_timestamp', None)
            flash('Password reset successfully. Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('User not found.', 'error')

    return render_template('reset_password.html')

@app.route('/logout')
def logout():
    username = session.get('user', 'Unknown')
    session.pop('user', None)
    session.pop('user_id', None)
    logger.info(f"User {username} logged out successfully")
    return redirect(url_for('welcome'))

@app.route('/delete_post/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401

    user = User.query.filter_by(username=session['user']).first()
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404

    post = Post.query.filter_by(id=post_id, user_id=user.id).first()
    if not post:
        return jsonify({'success': False, 'message': 'Post not found or not owned by user'}), 404

    # Delete the file if it exists
    if post.video_path:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'posts', post.video_path)
        if os.path.exists(file_path):
            os.remove(file_path)

    # Delete the post from database
    db.session.delete(post)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Post deleted successfully'})

@app.route('/predict', methods=['POST'])
def predict():
    global activity_duration
    data = request.get_json()
    image_data = data['image']
    selected_activities = data.get('selected_activities', classes)  # Default to all if not specified
    logger.info(f"Prediction request received. Selected activities: {selected_activities}")
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
    logger.info(f"Predicted activity: {activity}, Score: {score}")

    return jsonify({'activity': activity, 'score': score})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
