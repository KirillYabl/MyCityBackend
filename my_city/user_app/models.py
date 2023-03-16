from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models

from .managers import UserManager

max_password_length = 20
min_password_length = 8

class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='email address', unique=True,)
    password = models.CharField(max_length=150,
                                verbose_name='password',
                                validators=(MinLengthValidator(min_password_length),
                                            MaxLengthValidator(max_password_length),
                                            )
                                )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email
