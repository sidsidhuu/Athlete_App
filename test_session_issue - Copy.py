from flask import Flask, session
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'test'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

with app.test_request_context():
    session['user_id'] = 123
    session['user'] = 'testuser'
    print('Session set successfully')
    print('user_id:', session.get('user_id'))
    print('user:', session.get('user'))
