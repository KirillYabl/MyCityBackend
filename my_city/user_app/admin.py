from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminBase
from django.utils.translation import gettext_lazy as _

from . import models as m
from .forms import UserChangeForm, UserCreationForm


@admin.register(m.User)
class UserAdmin(UserAdminBase):
    add_form = UserCreationForm
    form = UserChangeForm
    model = m.User
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    list_display = ('email', 'is_staff', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)


@admin.register(m.Team)
class TeamAdmin(admin.ModelAdmin):
    pass


@admin.register(m.Member)
class MemberAdmin(admin.ModelAdmin):
    pass
