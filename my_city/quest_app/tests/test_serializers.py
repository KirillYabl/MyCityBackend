import pytest
from django.utils import timezone

from quest_app.choices import QuestStatus
from quest_app.models import Category, Quest
from quest_app.serializers import CategorySerializer, QuestSerializer


@pytest.mark.django_db()
class TestQuestSerializer:
    def test_quest_serializer(self):
        now = timezone.now()
        quest = Quest.objects.create(
            name="Test Quest",
            registration_start_at=now - timezone.timedelta(days=1),
            start_at=now + timezone.timedelta(days=1),
            end_at=now + timezone.timedelta(days=2),
            stop_show_at=now + timezone.timedelta(days=3),
        )
        quest = Quest.objects.with_status().get(id=quest.id)
        serializer = QuestSerializer(quest)
        data = serializer.data
        assert data['name'] == 'Test Quest'
        assert data['status'] == QuestStatus.coming


@pytest.mark.django_db()
class TestCategorySerializer:
    def test_category_serializer(self):
        now = timezone.now()
        quest = Quest.objects.create(
            name="Test Quest",
            registration_start_at=now - timezone.timedelta(days=1),
            start_at=now + timezone.timedelta(days=1),
            end_at=now + timezone.timedelta(days=2),
            stop_show_at=now + timezone.timedelta(days=3),
        )
        category = Category.objects.create(
            name='Test category',
            quest=quest,
            short_description='Test short description',
            long_description='Test long description' * 100,
            participation_order=1,
            results_order=1,
        )
        serializer = CategorySerializer(category)
        data = serializer.data
        assert data['name'] == 'Test category'
        assert data['long_description'] == 'Test long description' * 100
