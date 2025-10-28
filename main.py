import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from utils.performance import calculate_performance
import time

# Load model
model = load_model('models/activity_model.h5')

# Class names
classes = ['running', 'walking', 'squats', 'pushups', 'jumping_jacks', 'stretching']

# Open webcam
cap = cv2.VideoCapture(0)
start_time = time.time()
activity_duration = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess frame
    img = cv2.resize(frame, (64,64))
    img = img.astype('float') / 255.0
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)

    # Predict activity
    prediction = model.predict(img)
    activity = classes[np.argmax(prediction)]

    # Calculate duration for performance scoring
    current_time = time.time()
    activity_duration += 1/30  # assuming 30 FPS approx

    # Performance score
    score = calculate_performance(activity, duration_sec=activity_duration)

    # Display
    cv2.putText(frame, f'Activity: {activity}', (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    cv2.putText(frame, f'Performance Score: {score}', (20,80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,0), 2)

    cv2.imshow("Athlete Activity Recognition", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
