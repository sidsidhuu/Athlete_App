from flask import Flask
from models import db, init_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/athlete_app.db'
init_db(app)

with app.app_context():
    users = User.query.all()
    print('Users in DB:', len(users))
