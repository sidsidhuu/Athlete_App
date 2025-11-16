import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from utils.performance import calculate_performance
import time

print("Starting main.py with activity recognition")

# Load model
try:
    model = load_model('models/activity_model.h5')
    print("Model loaded successfully")
except Exception as e:
    print(f"Model loading failed: {e}. Using dummy predictions.")
    model = None

# Class names
classes = ['running', 'walking', 'squats', 'pushups', 'jumping_jacks', 'stretching']

# Open webcam
print("Attempting to open camera...")
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera. Please check camera permissions or if another application is using it.")
    exit()

print("Camera opened successfully")
start_time = time.time()
activity_duration = 0
frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to read frame from camera")
        break

    frame_count += 1

    # Preprocess frame for activity recognition
    img = cv2.resize(frame, (64,64))
    img = img.astype('float') / 255.0
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)

    # Predict activity
    if model:
        prediction = model.predict(img, verbose=0)
        activity = classes[np.argmax(prediction)]
        confidence = np.max(prediction)
    else:
        # Dummy prediction for demo
        activity = classes[frame_count % len(classes)]
        confidence = 0.5

    # Calculate duration for performance scoring
    current_time = time.time()
    activity_duration += 1  # increment per prediction

    # Performance score
    score = calculate_performance(activity, duration_sec=activity_duration)

    # Display activity and score
    cv2.putText(frame, f'Activity: {activity}', (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, f'Score: {score:.1f}', (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
    cv2.putText(frame, f'Confidence: {confidence:.2f}', (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 2)
    cv2.putText(frame, "Press 'q' to quit", (20, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Display the frame in a window
    cv2.imshow('Activity Recognition', frame)
    print(f"Frame {frame_count} processed, Activity: {activity}, Score: {score:.1f}")

    # Check for key press
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        print("Quitting...")
        break

cap.release()
cv2.destroyAllWindows()
print("Camera released and windows destroyed")
