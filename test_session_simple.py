from flask import Flask, session
app = Flask(__name__)
app.secret_key = 'test'
app.config['SESSION_TYPE'] = 'filesystem'
from flask_session import Session
Session(app)

with app.test_request_context():
    session['test'] = 'value'
    print('Session write works')
    print('Session value:', session.get('test'))
