from flask import Flask
from models import db, init_db, User
from werkzeug.security import check_password_hash
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath('instance/athlete_app.db')
init_db(app)

with app.app_context():
    user = User.query.filter_by(username='testuser').first()
    print('User found:', user.username if user else 'None')
    if user:
        print('Password check:', check_password_hash(user.password, 'testpass'))
        print('Password check wrong:', check_password_hash(user.password, 'wrongpass'))
