from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
import pickle


@api_view(['POST'])
def upload(request):
    file = request.FILES.get('file')
    event_id = request.POST.get('event_id')

    if not file:
        return Response({"status": "error", "message": "No file uploaded!"}, status=400)

    stored_faces = load_embeddings(event_id)


    
    return Response({"status": "success", "message": "File uploaded successfully!"})


def load_embeddings(event_id: str):
    embeddings_file = f"data/events/{event_id}/face_data.pkl"

    if not os.path.exists(embeddings_file):
        print(f"Embeddings file for event {event_id} not found.")

    with open(embeddings_file, "rb") as f:
        return pickle.load(f)
