from django_filters import rest_framework as filters

from .choices import QuestStatus
from .models import Quest


class QuestFilter(filters.FilterSet):
    status = filters.ChoiceFilter(choices=QuestStatus.choices)

    class Meta:
        model = Quest
        fields = ['status', ]
