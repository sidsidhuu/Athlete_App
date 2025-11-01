import requests

# Test register via HTTP - app should already be running
try:
    print('Testing real HTTP POST to /register...')
    response = requests.post('http://localhost:5000/register', data={
        'username': 'testuser10',
        'email': 'test10@example.com',
        'height': '170',
        'weight': '70',
        'password': 'testpass10'
    }, allow_redirects=True)  # Follow redirects

    print('Response status:', response.status_code)
    print('Response headers:', dict(response.headers))
    print('Response text:', response.text[:500])  # First 500 chars

except Exception as e:
    print('Error:', str(e))
    import traceback
    traceback.print_exc()
