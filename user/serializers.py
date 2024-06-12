from rest_framework import serializers
from .models import AuthUser
from . import utils


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ["username", "email", "first_name", "last_name", "password"]

    def validate_username(self, value):
        if not utils.is_valid_user_name(value):
            raise serializers.ValidationError("Invalid Username")
        return value

    def validate_email(self, value):
        if not utils.is_valid_email_id(value):
            raise serializers.ValidationError("Invalid email id")
        return value

    def validate_first_name(self, value):
        if not value or len(value) == 0:
            raise serializers.ValidationError("Invalid first name")
        return value

    def validate_last_name(self, value):
        if not value or len(value) == 0:
            raise serializers.ValidationError("Invalid last name")
        return value

    def validate_password(self, value):
        if not utils.is_valid_password(value):
            raise serializers.ValidationError("Invalid password")
        return value

    def create(self, validated_data):
        user = AuthUser(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
