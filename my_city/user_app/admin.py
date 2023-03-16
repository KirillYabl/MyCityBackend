from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminBase

from .forms import UserChangeForm, UserCreationForm
from .models import User


@admin.register(User)
class UserAdmin(UserAdminBase):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active',)
    search_fields = ('email',)
    ordering = ('email',)


