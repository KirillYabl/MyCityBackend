from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User

class CustomUserCreationForm(UserCreationForm):
    model = User
    fields = ['email',]

class CustomUserChangeForm(UserChangeForm):
    model = User
    fields = ['email',]


