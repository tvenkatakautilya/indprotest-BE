import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer


@api_view(["POST"])
def register(request):
    try:
        data = json.loads(request.body.strip())
    except json.JSONDecodeError:
        return Response(
            {"Message": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST
        )

    serializer = RegisterSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            {"Message": "User registered successfully"}, status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
