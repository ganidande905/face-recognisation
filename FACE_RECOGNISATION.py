import random
import cv2
import time
import numpy as np

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

num = 0

def smile_meter(frame, x1, y1):
    global num
    if num > 100:  # Reduced the threshold for resetting smile percentage
        x = str(random.randint(0, 100))
        font = cv2.FONT_HERSHEY_SIMPLEX
        color = (255, 0, 255)
        text = cv2.putText(frame, "Your smile is", (int(x1) + 15, int(y1) - 70), font, 1, color, 4, cv2.LINE_AA)
        text = cv2.putText(frame, x + "%", (int(x1) + 50, int(y1) - 20), font, 1, color, 4, cv2.LINE_AA)
        time.sleep(5)  # Reduced the sleep time for testing
        num = 0
        return num
    else:
        x = str(random.randint(0, 100))
        font = cv2.FONT_HERSHEY_SIMPLEX
        color = (255, 0, 255)
        text = cv2.putText(frame, "Smile Meter", (int(x1) + 15, int(y1) - 70), font, 1, color, 4, cv2.LINE_AA)
        text = cv2.putText(frame, x + "%", (int(x1) + 50, int(y1) - 20), font, 1, color, 4, cv2.LINE_AA)
        num = num + 5
        return num

# Initialize the webcam
video = cv2.VideoCapture(0)

if not video.isOpened():
    print("Error: Could not open video capture.")
else:
    while True:
        ret, frame = video.read()

        if not ret:
            print("Failed to retrieve frame from the webcam.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), -1)
            smiles = smile_cascade.detectMultiScale(gray[y:y + h, x:x + w], scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

            for (x1, y1, w1, h1) in smiles:
                cv2.rectangle(frame, (x + x1, y + y1), (x + x1 + w1, y + y1 + h1), (255, 0, 0), 3)
                num = smile_meter(frame, x + x1, y + y1)

        cv2.imshow("Smile Meter", frame)

        # Check for key press to exit
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    video.release()
    cv2.destroyAllWindows()

