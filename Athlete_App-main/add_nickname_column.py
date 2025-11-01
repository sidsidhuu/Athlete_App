from sqlalchemy import create_engine, text
import os

# Path to the database
db_path = os.path.abspath('instance/athlete_app.db')
engine = create_engine(f'sqlite:///{db_path}')

with engine.connect() as conn:
    # Add the nickname column
    conn.execute(text("ALTER TABLE user ADD COLUMN nickname VARCHAR(80)"))
    conn.commit()
    print("Added nickname column to user table.")
