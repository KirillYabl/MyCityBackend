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


@admin.register(m.Quest)
class Quest(admin.ModelAdmin):
    pass


@admin.register(m.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(m.AnswerType)
class AnswerTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(m.Assignment)
class Assignment(admin.ModelAdmin):
    pass


@admin.register(m.AnswerAttempt)
class AnswerAttemptAdmin(admin.ModelAdmin):
    pass
