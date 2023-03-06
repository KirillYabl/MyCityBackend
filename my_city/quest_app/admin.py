from django.contrib import admin

from . import models as m


@admin.register(m.ContactType)
class ContactTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(m.Contact)
class ContactAdmin(admin.ModelAdmin):
    pass


@admin.register(m.FAQ)
class FAQAdmin(admin.ModelAdmin):
    pass
