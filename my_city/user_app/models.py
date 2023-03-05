from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=10)
