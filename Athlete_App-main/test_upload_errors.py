import requests

# Test error cases for profile photo upload
def test_upload_errors():
    session = requests.Session()

    # Login first
    login_response = session.post('http://localhost:5000/login', data={
        'username': 'testuser10',
        'password': 'testpass10'
    }, allow_redirects=True)

    print('Login status:', login_response.status_code)

    # Test 1: No file provided
    upload_response = session.post('http://localhost:5000/upload_profile_photo', files={})
    print('No file test - Status:', upload_response.status_code)
    print('No file test - Response:', upload_response.json())

    # Test 2: Invalid file type (text file)
    files = {'profile_photo': ('test.txt', b'Hello world', 'text/plain')}
    upload_response = session.post('http://localhost:5000/upload_profile_photo', files=files)
    print('Invalid file type test - Status:', upload_response.status_code)
    print('Invalid file type test - Response:', upload_response.json())

    # Test 3: Empty filename
    files = {'profile_photo': ('', b'fake image data', 'image/jpeg')}
    upload_response = session.post('http://localhost:5000/upload_profile_photo', files=files)
    print('Empty filename test - Status:', upload_response.status_code)
    print('Empty filename test - Response:', upload_response.json())

if __name__ == '__main__':
    test_upload_errors()
