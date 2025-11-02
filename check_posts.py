import sqlite3

conn = sqlite3.connect('instance/athlete_app.db')
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables:")
for table in tables:
    print(table[0])

# Check post table
cursor.execute("SELECT COUNT(*) FROM post")
count = cursor.fetchone()
print(f"Posts count: {count[0]}")

cursor.execute("SELECT * FROM post LIMIT 5")
posts = cursor.fetchall()
print("Sample posts:")
for post in posts:
    print(post)

conn.close()
