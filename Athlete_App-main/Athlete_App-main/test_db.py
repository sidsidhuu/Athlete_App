from flask import Flask
from models import db, init_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/athlete_app.db'
init_db(app)

with app.app_context():
    try:
        db.create_all()
        print('Database tables created successfully')
    except Exception as e:
        print('Error:', e)
