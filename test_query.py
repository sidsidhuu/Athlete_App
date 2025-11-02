from flask import Flask
from models import db, init_db, User
import os

print('Current working directory:', os.getcwd())
print('Database file exists:', os.path.exists('instance/athlete_app.db'))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/athlete_app.db'
init_db(app)

with app.app_context():
    try:
        user = User.query.first()
        print('First user:', user)
    except Exception as e:
        print('Error querying user:', e)
        import traceback
        traceback.print_exc()
