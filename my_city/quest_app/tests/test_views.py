import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from quest_app.choices import QuestStatus
from quest_app.models import Quest


@pytest.mark.django_db()
class TestQuestAPI:

    def test_list_quest(self, quests):
        response = APIClient().get(reverse('quest-list'))
        assert response.status_code == 200
        data = response.json()
        now_show_quests = 2
        display_statuses = {QuestStatus.coming, QuestStatus.active, QuestStatus.finished}
        assert len(data['results']) == len(quests) - now_show_quests
        assert data['count'] == len(quests) - now_show_quests
        assert {quest['status'] for quest in data['results']} == display_statuses

    def test_filter_quests_by_status(self, quests):  # noqa: ARG002
        url = reverse('quest-list')
        response = APIClient().get(url, data={'status': QuestStatus.finished})
        data = response.json()
        assert response.status_code == 200
        assert len(data['results']) == 2
        assert data['count'] == 2
        assert data['results'][0]['name'] in ['Finished Quest', 'Finished stop none Quest']
        assert data['results'][1]['name'] in ['Finished Quest', 'Finished stop none Quest']

    def test_retrieve_quest(self, quests):
        coming_quest = quests[0]
        url = reverse('quest-detail', args=[coming_quest.pk])
        response = APIClient().get(url)
        assert response.status_code == 200
        assert response.data['name'] == coming_quest.name

    def test_retrieve_nonexistent_quest(self):
        nonexistent_id = Quest.objects.count() + 1
        url = reverse('quest-detail', args=[nonexistent_id])
        response = APIClient().get(url)
        assert response.status_code == 404
        assert response.data['detail'].code == 'not_found'


@pytest.mark.django_db()
class TestQuestCategoryAPI:

    def test_list_category(self, quests):
        active_quest = quests[1]
        categories = active_quest.categories.all()
        categories_count = categories.count()
        response = APIClient().get(reverse('quest-categories-list', args=[active_quest.pk]))
        assert response.status_code == 200
        data = response.json()
        assert len(data) == categories_count
        assert {name[0] for name in categories.values_list('name').distinct()} == {
            category['name'] for category in data}

    def test_nonexistent_quest_list_category(self):
        nonexistent_index = Quest.objects.count() + 1
        response = APIClient().get(reverse('quest-categories-list', args=[nonexistent_index]))
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0
        assert data == []

    def test_retrieve_category(self, quests):
        coming_quest = quests[0]
        category = coming_quest.categories.first()
        url = reverse('quest-categories-detail', args=[coming_quest.pk, category.pk])
        response = APIClient().get(url)
        assert response.status_code == 200
        assert response.data['name'] == category.name

    def test_retrieve_nonexistent_category(self, quests):
        coming_quest = quests[0]
        nonexistent_id = coming_quest.categories.count() + 1
        url = reverse('quest-categories-detail', args=[coming_quest.pk, nonexistent_id])
        response = APIClient().get(url)
        assert response.status_code == 404
        assert response.data['detail'].code == 'not_found'
