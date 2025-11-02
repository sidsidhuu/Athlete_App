import requests

# Test login via HTTP - app should already be running
try:
    print('Testing real HTTP POST to /login...')
    response = requests.post('http://localhost:5000/login', data={
        'username': 'testuser10',
        'password': 'testpass10'
    }, allow_redirects=True)  # Follow redirects

    print('Response status:', response.status_code)
    print('Response headers:', dict(response.headers))
    print('Response text:', response.text[:500])  # First 500 chars

except Exception as e:
    print('Error:', str(e))
    import traceback
    traceback.print_exc()
