import pytest
from django.utils import timezone

from quest_app.models import Quest
from quest_app.choices import QuestStatus
from quest_app.serializers import QuestSerializer


@pytest.mark.django_db
def test_quest_serializer():
    now = timezone.now()
    quest = Quest.objects.create(
        name="Test Quest",
        registration_start_at=now - timezone.timedelta(days=1),
        start_at=now + timezone.timedelta(days=1),
        end_at=now + timezone.timedelta(days=2),
        stop_show_at=now + timezone.timedelta(days=3)
    )
    quest = Quest.objects.with_status().get(id=quest.id)
    serializer = QuestSerializer(quest)
    data = serializer.data
    assert data['name'] == 'Test Quest'
    assert data['status'] == QuestStatus.coming
