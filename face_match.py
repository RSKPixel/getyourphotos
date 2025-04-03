import face_recognition
import pickle
import numpy as np
import os
from PIL import Image

# Define paths
PHOTO_DIR = "event-0001"
EMBEDDINGS_FILE = os.path.join(PHOTO_DIR, "face_data.pkl")
SELFIE_FILE = "selfi/selfie_resized.jpg"  # Replace with the actual selfie file


def find_matching_photo():
    # Load stored embeddings
    with open(EMBEDDINGS_FILE, "rb") as f:
        face_data = pickle.load(f)

    # Load selfie and extract embedding
    print(f"Processing selfie: {SELFIE_FILE}...")
    selfie_image = face_recognition.load_image_file(SELFIE_FILE)
    # selfie_encoding = face_recognition.face_encodings(selfie_image)
    selfie_encoding = face_recognition.face_encodings(selfie_image, model="cnn")

    if not selfie_encoding:
        print("❌ No face detected in the selfie.")
        return
    
    selfie_encoding = selfie_encoding[0]  # Only take the first detected face

    # Compare with stored embeddings
    best_match = None
    best_distance = float("inf")

    for entry in face_data:
        stored_encoding = entry["embedding"]
        distance = np.linalg.norm(stored_encoding - selfie_encoding)  # Euclidean distance

        if distance < best_distance:
            best_distance = distance
            best_match = entry["filename"]

    # Print result
    if best_match and best_distance < 0.6:  # Threshold for a good match
        print(f"✅ Best match found: {best_match} (Distance: {best_distance:.4f})")
    else:
        print("❌ No close match found.")

# Run the function
if __name__ == "__main__":
    find_matching_photo()
