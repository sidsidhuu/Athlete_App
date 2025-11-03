from PIL import Image

# Resize screenshot-wide.png to 1280x720
im = Image.open('static/screenshots/screenshot-wide.png')
im = im.resize((1280, 720), Image.LANCZOS)
im.save('static/screenshots/screenshot-wide.png', format='PNG', optimize=True)
print("Saved static/screenshots/screenshot-wide.png (1280x720)")

# Resize screenshot-narrow.png to 720x1280
im2 = Image.open('static/screenshots/screenshot-narrow.png')
im2 = im2.resize((720, 1280), Image.LANCZOS)
im2.save('static/screenshots/screenshot-narrow.png', format='PNG', optimize=True)
print("Saved static/screenshots/screenshot-narrow.png (720x1280)")
