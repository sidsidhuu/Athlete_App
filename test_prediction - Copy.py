import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

# Load model
model = load_model('models/activity_model.h5')

# Class names
classes = ['running', 'walking', 'squats', 'pushups', 'jumping_jacks', 'stretching']

# Open webcam
cap = cv2.VideoCapture(0)

ret, frame = cap.read()
if ret:
    # Preprocess frame
    img = cv2.resize(frame, (64,64))
    img = img.astype('float') / 255.0
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)

    # Predict activity
    prediction = model.predict(img)
    activity = classes[np.argmax(prediction)]
    confidence = np.max(prediction)

    print(f'Predicted Activity: {activity}')
    print(f'Confidence: {confidence}')
    print(f'All predictions: {prediction}')

    cv2.putText(frame, f'Activity: {activity}', (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    cv2.imshow("Test Frame", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Failed to capture frame")

cap.release()
