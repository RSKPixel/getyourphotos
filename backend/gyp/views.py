from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def upload(request):

    file = request.FILES.get('file')
    if not file:
        return Response({"status": "error", "message": "No file uploaded!"}, status=400)
    
    


    return Response({"status": "success", "message": "File uploaded successfully!"})