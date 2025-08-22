from django.db import models
from django.utils import timezone
import uuid

class PendingUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=128)  # Хранить хэш пароля
    email_confirmation_token = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    generated_password = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username
