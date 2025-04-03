from fastapi import FastAPI, File, UploadFile
import face_recognition
import numpy as np
import pickle
import cv2
import io
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow requests from your frontend (http://localhost:5175)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (or specify ["http://localhost:5175"])
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Load stored face embeddings
EMBEDDINGS_FILE = "events/E0001/face_data.pkl"
with open(EMBEDDINGS_FILE, "rb") as f:
    stored_faces = pickle.load(f)

@app.get("/")
async def root():
    return {"message": "Welcome to the Face Recognition API!"}


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Read image file
    image_bytes = await file.read()
    image_np = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    # Convert BGR to RGB (for face_recognition)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Get face encodings
    face_encodings = face_recognition.face_encodings(rgb_image)
    if not face_encodings:
        return {"message": "No face detected."}

    matches = []
    for encoding in face_encodings:
        for stored_face in stored_faces:
            match = face_recognition.compare_faces([stored_face["embedding"]], encoding, tolerance=0.6)
            if match[0]:
                matches.append(stored_face["filename"])

    return {"matches": list(set(matches))}

