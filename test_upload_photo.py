import requests
import os

# Test profile photo upload functionality
def test_upload_photo():
    # First, login to get session
    session = requests.Session()

    # Login
    login_response = session.post('http://localhost:5000/login', data={
        'username': 'testuser10',
        'password': 'testpass10'
    }, allow_redirects=True)

    print('Login status:', login_response.status_code)
    if login_response.status_code != 200:
        print('Login failed, trying to register first...')
        # Register first
        register_response = session.post('http://localhost:5000/register', data={
            'username': 'testuser10',
            'email': 'test10@example.com',
            'height': '170',
            'weight': '70',
            'password': 'testpass10'
        }, allow_redirects=True)
        print('Register status:', register_response.status_code)

    # Create a test image file
    test_image_path = 'test_image.jpg'
    with open(test_image_path, 'wb') as f:
        # Create a minimal JPEG file (1x1 pixel)
        f.write(b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9')

    # Test upload
    with open(test_image_path, 'rb') as f:
        files = {'profile_photo': ('test.jpg', f, 'image/jpeg')}
        upload_response = session.post('http://localhost:5000/upload_profile_photo', files=files)

    print('Upload status:', upload_response.status_code)
    print('Upload response:', upload_response.json())

    # Clean up
    if os.path.exists(test_image_path):
        os.remove(test_image_path)

if __name__ == '__main__':
    test_upload_photo()
