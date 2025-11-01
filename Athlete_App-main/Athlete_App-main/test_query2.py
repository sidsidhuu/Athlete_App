from flask import Flask
from models import db, init_db, User
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath('instance/athlete_app.db')
init_db(app)

with app.app_context():
    try:
        user = User.query.first()
        print('First user:', user)
    except Exception as e:
        print('Error:', e)
