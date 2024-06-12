from django.contrib.auth.models import AbstractUser
from django.db import models


class AuthUser(AbstractUser):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username
