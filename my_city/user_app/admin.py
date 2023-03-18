from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminBase

from . import models as m
from .forms import UserChangeForm, UserCreationForm


@admin.register(m.User)
class UserAdmin(UserAdminBase):
    add_form = UserCreationForm
    form = UserChangeForm
    model = m.User
    list_display = ('email', 'is_staff', 'is_active',)
    search_fields = ('email',)
    ordering = ('email',)


@admin.register(m.Team)
class TeamAdmin(admin.ModelAdmin):
    pass


@admin.register(m.Member)
class MemberAdmin(admin.ModelAdmin):
    pass


@admin.register(m.TeamMembership)
class TeamMembershipAdmin(admin.ModelAdmin):
    pass
