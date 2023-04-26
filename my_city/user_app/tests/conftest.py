import copy

import pytest

SUCCESS_DATA = {
    "email": "vasya@mail.ru",
    "password": "asd@$124Dsfd2",
    "team": {
        "name": "teamsdfkjskjsgb",
    },
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
}

EMPTY_DATA = {
    "email": "",
    "password": "",
    "team": {
        "name": "",
    },
    "members": [{}],
}


@pytest.fixture()
def success_registration_data():
    return SUCCESS_DATA


@pytest.fixture()
def error_registration_norequirement_data():
    return EMPTY_DATA


@pytest.fixture()
def error_registration_wrong_first_data():
    wrong_data = copy.deepcopy(SUCCESS_DATA)
    wrong_data['email'] = "vasyaru"
    wrong_data['password'] = "vasya"  # noqa: S105
    wrong_data['team'] = {"name": "teamsd   fkjskjsgb"}
    wrong_data['members'] = [
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
    wrong_data['members'] = [
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
    wrong_data['members'] = [
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
    wrong_data['members'] = [
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
    wrong_data['members'][1]['full_name'] = 'Иван Григорьевичasd'
    return wrong_data
