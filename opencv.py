import cv2
from PIL import Image


selfie_path = "selfi/selfie.jpg"
img = cv2.imread(selfie_path)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

if len(faces) > 0:
    print(f"✅ OpenCV detected {len(faces)} face(s).")
else:
    print("❌ No face detected with OpenCV.")
