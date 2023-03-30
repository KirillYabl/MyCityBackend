import os.path

import pytest
from django.utils import timezone

from quest_app.models import Quest


@pytest.fixture
def quests():
    now = timezone.now()
    coming_quest = Quest.objects.create(
        name="Coming Quest",
        registration_start_at=now - timezone.timedelta(days=1),
        start_at=now + timezone.timedelta(days=1),
        end_at=now + timezone.timedelta(days=2),
        stop_show_at=now + timezone.timedelta(days=3),
        address="Quest address",
        banner=os.path.join(Quest.banner.field.upload_to, 'default_picture.png'),
    )
    active_quest = Quest.objects.create(
        name="Active Quest",
        registration_start_at=now - timezone.timedelta(days=2),
        start_at=now - timezone.timedelta(days=1),
        end_at=now + timezone.timedelta(days=1),
        stop_show_at=now + timezone.timedelta(days=2),
        address="Quest address",
        banner=os.path.join(Quest.banner.field.upload_to, 'default_picture.png'),
    )
    finished_quest = Quest.objects.create(
        name="Finished Quest",
        registration_start_at=now - timezone.timedelta(days=3),
        start_at=now - timezone.timedelta(days=2),
        end_at=now - timezone.timedelta(days=1),
        stop_show_at=now + timezone.timedelta(days=1),
        address="Quest address",
        banner=os.path.join(Quest.banner.field.upload_to, 'default_picture.png'),
    )
    not_showing_quest = Quest.objects.create(
        name="Not Showing Quest",
        registration_start_at=now + timezone.timedelta(days=1),
        start_at=now + timezone.timedelta(days=2),
        end_at=now + timezone.timedelta(days=3),
        stop_show_at=now + timezone.timedelta(days=4),
        address="Quest address",
        banner=os.path.join(Quest.banner.field.upload_to, 'default_picture.png'),
    )
    expired_quest = Quest.objects.create(
        name="Expired Quest",
        registration_start_at=now - timezone.timedelta(days=4),
        start_at=now - timezone.timedelta(days=3),
        end_at=now - timezone.timedelta(days=2),
        stop_show_at=now - timezone.timedelta(days=1),
        address="Quest address",
        banner=os.path.join(Quest.banner.field.upload_to, 'default_picture.png'),
    )
    finished_stop_none_quest = Quest.objects.create(
        name="Finished stop none Quest",
        registration_start_at=now - timezone.timedelta(days=3),
        start_at=now - timezone.timedelta(days=2),
        end_at=now - timezone.timedelta(days=1),
        address="Quest address",
        banner=os.path.join(Quest.banner.field.upload_to, 'default_picture.png'),
    )
    return [coming_quest, active_quest, finished_quest, not_showing_quest, expired_quest, finished_stop_none_quest]
