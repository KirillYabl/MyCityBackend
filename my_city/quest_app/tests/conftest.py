import os.path

import pytest
from django.utils import timezone
from django.conf import settings

from quest_app.models import Quest, Category


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

    categories = []
    for i in range(5):
        categories.append(
            Category(
                name=f'Test category {i}',
                quest=coming_quest,
                short_description=f'Test short description {i}',
                long_description=f'Test long description {i}' * 100,
                participation_order=i + 1,
                results_order=5 - i,
            )
        )
    for i in range(settings.REST_FRAMEWORK['PAGE_SIZE'] + 1):
        categories.append(
            Category(
                name=f'Test category {i}',
                quest=active_quest,
                short_description=f'Test short description {i}',
                long_description=f'Test long description {i}' * 100,
                participation_order=i + 1,
                results_order=i + 1,
            )
        )
    Category.objects.bulk_create(categories)
    return [coming_quest, active_quest, finished_quest, not_showing_quest, expired_quest, finished_stop_none_quest]
