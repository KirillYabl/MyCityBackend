import pytest

from quest_app.choices import QuestStatus
from quest_app.models import Quest


@pytest.mark.django_db()
class TestQuestQueryset:
    def test_quest_queryset_which_show(self, quests):  # noqa: ARG002
        assert Quest.objects.which_show().count() == 4

    def test_quest_queryset_with_status(self, quests):
        coming_quest = quests[0]
        active_quest = quests[1]
        finished_quest = quests[2]

        quests = Quest.objects.with_status()
        assert quests.get(id=coming_quest.id).status == QuestStatus.coming
        assert quests.get(id=active_quest.id).status == QuestStatus.active
        assert quests.get(id=finished_quest.id).status == QuestStatus.finished
