from models import db, init_db
from flask import Flask
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath('instance/athlete_app.db')
init_db(app)

with app.app_context():
    db.create_all()
    print("Database updated with new schema.")
