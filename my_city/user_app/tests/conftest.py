import copy
import os

import pytest
from django.utils import timezone
from quest_app.models import Category, Quest

SUCCESS_DATA = {
    "email": "vasya@mail.ru",
    "password": "asd@$124Dsfd2",
    "team": {
        "name": "teamsdfkjskjsgb",
        "members": [
            {
                "full_name": "Василий Петрович",
                "birth_date": "1978-02-15",
                "phone": "+79003457896",
                "email": "vasya@mail.ru",
                "is_captain": True,
                "member_number": 1,
            },
            {
                "full_name": "Иван Григорьевич",
                "birth_date": "1975-02-15",
                "phone": "+79003452896",
                "email": "vasaya@mail.ru",
                "is_captain": False,
                "member_number": 2,
            },
        ],
    },
}

SUCCESS_ANOTHER_DATA = {
    "email": "petya@mail.ru",
    "password": "asd@$124Dsfd2",
    "team": {
        "name": "teamsd32fkjskjsgb",
        "members": [
            {
                "full_name": "Василий Петрович",
                "birth_date": "1978-02-15",
                "phone": "+79003457896",
                "email": "petya@mail.ru",
                "is_captain": True,
                "member_number": 1,
            },
            {
                "full_name": "Иван Григорьевич",
                "birth_date": "1975-02-15",
                "phone": "+79003452896",
                "email": "vasaya@mail.ru",
                "is_captain": False,
                "member_number": 2,
            },
        ],
    },
}

EMPTY_DATA = {
    "email": "",
    "password": "",
    "team": {
        "name": "",
        "members": [{}],
    },
}


@pytest.fixture()
def success_registration_data():
    return SUCCESS_DATA


@pytest.fixture()
def success_registration_another_data():
    return SUCCESS_ANOTHER_DATA


@pytest.fixture()
def error_registration_norequirement_data():
    return EMPTY_DATA


@pytest.fixture()
def error_registration_wrong_first_data():
    wrong_data = copy.deepcopy(SUCCESS_DATA)
    wrong_data['email'] = "vasyaru"
    wrong_data['password'] = "vasya"  # noqa: S105
    wrong_data['team']['name'] = "teamsd   fkjskjsgb"
    wrong_data['team']['members'] = [
        {
            "full_name": "vasya",
            "birth_date": "197815",
            "phone": "89003457896",
            "email": "vasya@mail.ru",
            "is_captain": "s",
            "member_number": 10,
        },
        {
            "full_name": "Иван Григорьевич Иван Григорьевич Иван Григорьевич",
            "birth_date": "1775-02-15",
            "phone": "+790034528",
            "email": "vasayaru",
            "is_captain": False,
            "member_number": "asd",
        },
    ]
    return wrong_data


@pytest.fixture()
def error_registration_wrong_second_data():
    wrong_data = copy.deepcopy(SUCCESS_DATA)
    wrong_data['team']['members'] = [
        {
            "full_name": "Василий Петрович",
            "birth_date": "1978-02-15",
            "phone": "",
            "email": "asdvasya@mail.ru",
            "is_captain": False,
            "member_number": 1,
        },
        {
            "full_name": "Иван Григорьевич",
            "birth_date": "1975-02-15",
            "phone": "",
            "email": "",
            "is_captain": False,
            "member_number": 2,
        },
        {
            "full_name": "Иван Григорьевич",
            "birth_date": "1975-02-15",
            "phone": "+79003452896",
            "email": "vasaya@mail.ru",
            "is_captain": True,
            "member_number": 4,
        },
        {
            "full_name": "Иван Григорьевич",
            "birth_date": "1975-02-15",
            "phone": "+79003452896",
            "email": "vasaya@mail.ru",
            "is_captain": False,
            "member_number": 5,
        },
    ]
    return wrong_data


@pytest.fixture()
def error_registration_wrong_members_general_other_data():
    wrong_data = copy.deepcopy(SUCCESS_DATA)
    wrong_data['team']['members'] = [
        {
            "full_name": "Василий Петрович",
            "birth_date": "1978-02-01",
            "phone": "+79003457896",
            "email": "ivasya@mail.ru",
            "is_captain": True,
            "member_number": 1,
        },
        {
            "full_name": "Василий Петрович",
            "birth_date": "1978-02-02",
            "phone": "+79003457896",
            "email": "ivasya@mail.ru",
            "is_captain": False,
            "member_number": 2,
        },
        {
            "full_name": "Василий Петрович",
            "birth_date": "1978-02-03",
            "phone": "+79003457896",
            "email": "ivasya@mail.ru",
            "is_captain": False,
            "member_number": 3,
        },
        {
            "full_name": "Василий Петрович",
            "birth_date": "1978-02-04",
            "phone": "+79003457896",
            "email": "ivasya@mail.ru",
            "is_captain": False,
            "member_number": 5,
        },
        {
            "full_name": "Василий Петрович",
            "birth_date": "1978-02-05",
            "phone": "+79003457896",
            "email": "ivasya@mail.ru",
            "is_captain": False,
            "member_number": 5,
        },
        {
            "full_name": "Василий Петрович",
            "birth_date": "1978-02-06",
            "phone": "+79003457896",
            "email": "ivasya@mail.ru",
            "is_captain": False,
            "member_number": 5,
        },
    ]
    return wrong_data


@pytest.fixture()
def error_registration_wrong_members_general_captain_data():
    wrong_data = copy.deepcopy(SUCCESS_DATA)
    wrong_data['team']['members'] = [
        {
            "full_name": "Василий Петрович",
            "birth_date": "1978-02-15",
            "phone": "+79003457896",
            "email": "vasya@mail.ru",
            "is_captain": True,
            "member_number": 1,
        },
    ]
    return wrong_data


@pytest.fixture()
def error_registration_invalid_full_name():
    wrong_data = copy.deepcopy(SUCCESS_DATA)
    wrong_data['team']['members'][1]['full_name'] = 'Иван Григорьевичasd'
    return wrong_data


@pytest.fixture()
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

    categories = []
    for quest in [coming_quest, active_quest]:
        for i in range(5):
            categories.append(
                Category(
                    name=f'Test category {i}',
                    quest=quest,
                    short_description=f'Test short description {i}',
                    long_description=f'Test long description {i}' * 100,
                    participation_order=i + 1,
                    results_order=5 - i,
                ),
            )
    Category.objects.bulk_create(categories)
    return [coming_quest, active_quest]
