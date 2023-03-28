from django.db import models


class QuestStatus(models.TextChoices):
    coming = 'coming'
    active = 'active'
    finished = 'finished'
