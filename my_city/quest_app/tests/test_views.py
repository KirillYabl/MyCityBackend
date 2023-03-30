import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from quest_app.choices import QuestStatus


@pytest.mark.django_db
class TestQuestAPI:

    def test_list_quest(self, quests):
        response = APIClient().get(reverse('quest-list'))
        assert response.status_code == 200
        data = response.json()
        now_show_quests = 2
        display_statuses = {QuestStatus.coming, QuestStatus.active, QuestStatus.finished}
        assert len(data['results']) == len(quests) - now_show_quests
        assert data['count'] == len(quests) - now_show_quests
        assert set(quest['status'] for quest in data['results']) == display_statuses

    def test_filter_quests_by_status(self, quests):
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
