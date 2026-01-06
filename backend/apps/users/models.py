from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    index_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    whatsapp_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.username