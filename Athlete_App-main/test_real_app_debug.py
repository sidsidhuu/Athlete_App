import requests
import threading
import time

# Start the app in a thread
def start_app():
    import subprocess
    subprocess.run(['python', 'app.py'])

# Start app in background
app_thread = threading.Thread(target=start_app, daemon=True)
app_thread.start()

# Wait for app to start
time.sleep(3)

# Test register via HTTP
try:
    print('Testing real HTTP POST to /register...')
    response = requests.post('http://localhost:5000/register', data={
        'username': 'testuser9',
        'email': 'test9@example.com',
        'height': '170',
        'weight': '70',
        'password': 'testpass9'
    }, allow_redirects=True)  # Follow redirects

    print('Response status:', response.status_code)
    print('Response headers:', dict(response.headers))
    print('Response text:', response.text[:500])  # First 500 chars

except Exception as e:
    print('Error:', str(e))
    import traceback
    traceback.print_exc()
