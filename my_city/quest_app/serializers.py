from rest_framework import serializers

from .choices import QuestStatus
from .models import Quest


class QuestSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=QuestStatus.choices)

    class Meta:
        model = Quest
        fields = (
            'id',
            'name',
            'description',
            'registration_start_at',
            'start_at',
            'end_at',
            'stop_show_at',
            'address',
            'banner',
            'status',
        )
