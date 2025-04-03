import cv2
import face_recognition
import numpy as np
import pickle

# Load face embeddings
EMBEDDINGS_FILE = "event-0001/face_data.pkl"
SELFIE_PATH = "selfi/20250116135203.jpg"

def detect_face_with_opencv(image_path):
    """ Detect faces using OpenCV's Haar cascade classifier """
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    return len(faces) > 0  # Returns True if at least one face is detected

def match_faces():
    # Load stored face embeddings
    with open(EMBEDDINGS_FILE, "rb") as f:
        known_faces = pickle.load(f)

    # Detect face in the selfie using OpenCV
    opencv_detected = detect_face_with_opencv(SELFIE_PATH)
    if not opencv_detected:
        print("❌ OpenCV: No face detected in the selfie.")
        return

    # Load the selfie
    selfie_image = face_recognition.load_image_file(SELFIE_PATH)
    selfie_encodings = face_recognition.face_encodings(selfie_image)

    if len(selfie_encodings) == 0:
        print("❌ face_recognition: No face detected in the selfie.")
        return
    
    print(f"🔍 Found {len(selfie_encodings)} face(s) in the selfie.")

    # Check each detected face in the selfie
    match_found = False
    for idx, selfie_encoding in enumerate(selfie_encodings):
        print(f"🔎 Checking face {idx + 1} in the selfie...")

        for face in known_faces:
            result = face_recognition.compare_faces([face["embedding"]], selfie_encoding, tolerance=0.5)
            if result[0]:
                print(f"✅ Match found: {face['filename']} (for face {idx + 1})")
                match_found = True
    
    if not match_found:
        print("❌ No match found.")

if __name__ == "__main__":
    match_faces()
