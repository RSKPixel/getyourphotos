from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
import pickle
import dlib
import numpy as np
import cv2
import face_recognition
from django.conf import settings

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def detect_face_with_opencv(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return len(faces) > 0, faces  # Returns True if at least one face is detected


@api_view(["POST"])
def upload(request):
    file = request.FILES.get("file")
    event_id = request.POST.get("event_id")

    if not file:
        return Response({"status": "error", "message": "No file uploaded!"})

    image_array = np.frombuffer(file.read(), dtype=np.uint8)
    uploaded_image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    # Detect face using OpenCV
    face_detected, faces = detect_face_with_opencv(uploaded_image)

    if not face_detected:
        return Response({"status": "error", "message": "No face detected in the uploaded image!"})

    # Encode face using face_recognition
    selfie_encodings = face_recognition.face_encodings(uploaded_image)

    if len(selfie_encodings) == 0:
        return Response({"status": "error", "message": "No face encoding found in the uploaded image!"})

    # Load stored face embeddings
    stored_faces = load_embeddings(event_id)

    if not stored_faces:
        return Response({"status": "error", "message": "No stored face data found for this event!"})

    match_found = False
    matched_filenames = []
    matched_files = []
    event_folder = f"{settings.MEDIA_URL}{event_id}/"  # Adjust as needed

    # Compare detected face with stored embeddings
    for selfie_encoding in selfie_encodings:
        for face in stored_faces:
            result = face_recognition.compare_faces([face["embedding"]], selfie_encoding, tolerance=0.5)
            if result[0]:
                matched_filenames.append(face["filename"])
                matched_files.append(event_folder + face["filename"])
                match_found = True

    if match_found:
        # remove duplicates
        matched_filenames = list(set(matched_filenames))
        matched_files = list(set(matched_files))
        return Response({"status": "success", "message": "Match found!", "matched_files": matched_files})
    else:
        return Response({"status": "error", "message": "No match found!"})


def load_embeddings(event_id: str):
    embeddings_file = f"data/media/{event_id}/face_data.pkl"

    if not os.path.exists(embeddings_file):
        print(f"Embeddings file for event {event_id} not found.")

    with open(embeddings_file, "rb") as f:
        return pickle.load(f)
