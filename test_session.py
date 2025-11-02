from flask import Flask, session
from flask_session import Session
from models import db, init_db
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath('instance/athlete_app.db')
init_db(app)

Session(app)

with app.test_request_context():
    try:
        print('Session initialized successfully')
        session['test'] = 'value'
        print('Session set:', session.get('test'))
    except Exception as e:
        print('Session error:', str(e))
        import traceback
        traceback.print_exc()
