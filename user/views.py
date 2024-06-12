import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


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


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh_token = response.data.get("refresh")
        access_token = response.data.get("access")
        if refresh_token and access_token:
            response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
        return response
