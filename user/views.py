import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import AuthUser
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status


import logging

logger = logging.getLogger(__name__)


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
        username = request.data.get("username")
        password = request.data.get("password")

        try:
            user = AuthUser.objects.get(username=username)
        except AuthUser.DoesNotExist:
            return Response({"detail": "User Does not exists"}, status=status.HTTP_401_UNAUTHORIZED)

        if not check_password(password, user.password):
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        response_data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        response = Response(response_data, status=status.HTTP_200_OK)
        response.set_cookie(key="refresh_token", value=str(refresh), httponly=True)
        return response