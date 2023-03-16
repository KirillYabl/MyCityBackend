from django.contrib.auth.forms import UserChangeForm as UserChangeFormBase
from django.contrib.auth.forms import UserCreationForm as UserFormBase

from .models import User


class UserCreationForm(UserFormBase):
    class Meta:
        model = User
        fields = ('email',)


class UserChangeForm(UserChangeFormBase):
    class Meta:
        model = User
        fields = ('email',)
