from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models

from .managers import UserManager

max_length = 20
min_length = 8

class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='email address',
                              unique=True,
                              validators=(MinLengthValidator(min_length), MaxLengthValidator(max_length),),
                              )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email
