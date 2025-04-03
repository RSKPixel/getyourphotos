import os
import face_recognition
import numpy as np
import pickle

# Define paths
PHOTO_DIR = "event-0001"  # Folder where wedding images are stored
EMBEDDINGS_FILE = os.path.join(PHOTO_DIR, "face_data.pkl")  # File to save embeddings

# Allowed image extensions
VALID_EXTENSIONS = (".jpg", ".jpeg", ".png")

def process_and_store_faces():
    face_data = []
    image_files = [f for f in os.listdir(PHOTO_DIR) if f.lower().endswith(VALID_EXTENSIONS)]

    print(f"Found {len(image_files)} images. Processing...")

    for idx, filename in enumerate(image_files, start=1):
        file_path = os.path.join(PHOTO_DIR, filename)

        try:
            # Load image
            print(f"({idx}/{len(image_files)}) Processing {filename}...")
            image = face_recognition.load_image_file(file_path)

            # Detect faces & extract embeddings
            face_encodings = face_recognition.face_encodings(image)

            for encoding in face_encodings:
                face_data.append({"embedding": encoding, "filename": filename})
        
        except Exception as e:
            print(f"⚠️ Skipping {filename}: {e}")

    # Save embeddings to a file
    if face_data:
        with open(EMBEDDINGS_FILE, "wb") as f:
            pickle.dump(face_data, f)
        print(f"✅ Processed {len(face_data)} faces and saved to {EMBEDDINGS_FILE}")
    else:
        print("❌ No faces found in any image.")

# Run the function
if __name__ == "__main__":
    process_and_store_faces()
