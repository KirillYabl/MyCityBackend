from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from . import models as m


@admin.register(m.User)
class UserAdmin(BaseUserAdmin):
    pass


@admin.register(m.Team)
class TeamAdmin(admin.ModelAdmin):
    pass


@admin.register(m.Member)
class MemberAdmin(admin.ModelAdmin):
    pass


@admin.register(m.TeamMembership)
class TeamMembershipAdmin(admin.ModelAdmin):
    pass
