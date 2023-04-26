import pytest
from django.urls import reverse
from knox.crypto import hash_token
from knox.models import AuthToken
from rest_framework.test import APIClient

from user_app.models import Member, Team, User


@pytest.mark.django_db()
class TestRegistrationAPI:
    def test_success(self, success_registration_data):
        users_cnt = User.objects.count()
        teams_cnt = Team.objects.count()
        members_cnt = Member.objects.count()
        response = APIClient().post(
            reverse('registration'), data=success_registration_data, format='json',
        )
        assert response.status_code == 200
        assert User.objects.count() == users_cnt + 1
        assert Team.objects.count() == teams_cnt + 1
        assert Member.objects.count() == members_cnt + \
            len(success_registration_data['team']['members'])
        new_user = User.objects.get(email=success_registration_data['email'])
        data = response.json()
        assert 'user' in data
        assert data['user']['email'] == new_user.email
        assert data['user']['id'] == new_user.id
        assert data['user']['email'] == success_registration_data['email']
        assert 'token' in data
        AuthToken.objects.get(user=new_user, digest=hash_token(data['token']))

    def test_empty(self, error_registration_norequirement_data):
        users_cnt = User.objects.count()
        teams_cnt = Team.objects.count()
        members_cnt = Member.objects.count()
        response = APIClient().post(
            reverse('registration'),
            data=error_registration_norequirement_data,
            format='json',
        )
        assert response.status_code == 400
        assert User.objects.count() == users_cnt
        assert Team.objects.count() == teams_cnt
        assert Member.objects.count() == members_cnt
        data = response.json()
        members = data['team']['members']
        assert 'This field may not be blank.' in data['email']
        assert 'This field may not be blank.' in data['password']
        assert 'This field may not be blank.' in data['team']['name']
        assert 'This field is required.' in members[0]['full_name']
        assert 'This field is required.' in members[0]['birth_date']
        assert 'This field is required.' in members[0]['is_captain']
        assert 'This field is required.' in members[0]['member_number']

    def test_first_invalid_data(self, error_registration_wrong_first_data):
        users_cnt = User.objects.count()
        teams_cnt = Team.objects.count()
        members_cnt = Member.objects.count()
        response = APIClient().post(
            reverse('registration'),
            data=error_registration_wrong_first_data,
            format='json',
        )
        assert response.status_code == 400
        assert User.objects.count() == users_cnt
        assert Team.objects.count() == teams_cnt
        assert Member.objects.count() == members_cnt
        data = response.json()
        members = data['team']['members']
        assert 'Enter a valid email address.' in data['email']
        assert 'Ensure this field has at least 8 characters.' in data['password']
        assert 'name' in data['team']
        assert len(members) == 2
        assert 'full_name' in members[0]
        assert 'birth_date' in members[0]
        assert 'phone' in members[0]
        assert 'is_captain' in members[0]
        assert 'member_number' in members[0]
        assert 'full_name' in members[1]
        assert 'phone' in members[1]
        assert 'email' in members[1]
        assert 'member_number' in members[1]

    def test_second_invalid_data(self, error_registration_wrong_second_data):
        users_cnt = User.objects.count()
        teams_cnt = Team.objects.count()
        members_cnt = Member.objects.count()
        response = APIClient().post(
            reverse('registration'), data=error_registration_wrong_second_data, format='json',
        )
        assert response.status_code == 400
        assert User.objects.count() == users_cnt
        assert Team.objects.count() == teams_cnt
        assert Member.objects.count() == members_cnt
        data = response.json()
        members = data['team']['members']
        assert len(members) == 4
        assert 'is_captain' in members[0]
        assert 'phone' in members[0]
        assert 'phone' in members[1]
        assert 'email' in members[1]
        assert 'is_captain' in members[2]
        assert 'full_name' in members[2]
        assert 'full_name' in members[3]

    def test_members_general_other_invalid_data(
        self, error_registration_wrong_members_general_other_data,
    ):
        users_cnt = User.objects.count()
        teams_cnt = Team.objects.count()
        members_cnt = Member.objects.count()
        response = APIClient().post(
            reverse('registration'),
            data=error_registration_wrong_members_general_other_data,
            format='json',
        )
        assert response.status_code == 400
        assert User.objects.count() == users_cnt
        assert Team.objects.count() == teams_cnt
        assert Member.objects.count() == members_cnt
        data = response.json()
        assert 'email для регистрации и у капитана должны совпадать' in data['members_general']
        assert 'Число участников должно быть от 2 до 5' in data['members_general']
        assert (
            'Между номерами участников не должно быть пропусков и повторов (от 1 до 6)'
            in data['members_general']
        )
        assert (
            'У всех участников, у которых задан email, они должны быть разными'
            in data['members_general']
        )
        assert (
            'У всех участников, у которых задан телефон, они должны быть разными'
            in data['members_general']
        )

    def test_members_general_captain_invalid_data(
        self,
        error_registration_wrong_members_general_captain_data,
    ):
        users_cnt = User.objects.count()
        teams_cnt = Team.objects.count()
        members_cnt = Member.objects.count()
        response = APIClient().post(
            reverse('registration'),
            data=error_registration_wrong_members_general_captain_data,
            format='json',
        )
        assert response.status_code == 400
        assert User.objects.count() == users_cnt
        assert Team.objects.count() == teams_cnt
        assert Member.objects.count() == members_cnt
        data = response.json()
        assert 'Число участников должно быть от 2 до 5' in data['members_general']

    def test_repeat_email(self, success_registration_data):
        users_cnt = User.objects.count()
        teams_cnt = Team.objects.count()
        members_cnt = Member.objects.count()
        response = APIClient().post(
            reverse('registration'), data=success_registration_data, format='json',
        )
        assert response.status_code == 200
        users_cnt += 1
        teams_cnt += 1
        members_cnt += len(success_registration_data['team']['members'])
        assert User.objects.count() == users_cnt
        assert Team.objects.count() == teams_cnt
        assert Member.objects.count() == members_cnt
        new_user = User.objects.get(email=success_registration_data['email'])
        data = response.json()
        assert 'user' in data
        assert data['user']['email'] == new_user.email
        assert data['user']['id'] == new_user.id
        assert data['user']['email'] == success_registration_data['email']
        assert 'token' in data
        AuthToken.objects.get(user=new_user, digest=hash_token(data['token']))
        response = APIClient().post(
            reverse('registration'), data=success_registration_data, format='json',
        )
        data = response.json()
        assert response.status_code == 400
        assert User.objects.count() == users_cnt
        assert Team.objects.count() == teams_cnt
        assert Member.objects.count() == members_cnt
        assert 'email' in data
        assert 'пользователь with this email address already exists.' in data['email']

    def test_invalid_full_name(self, error_registration_invalid_full_name):
        users_cnt = User.objects.count()
        teams_cnt = Team.objects.count()
        members_cnt = Member.objects.count()
        response = APIClient().post(
            reverse('registration'), data=error_registration_invalid_full_name, format='json',
        )
        assert response.status_code == 400
        assert User.objects.count() == users_cnt
        assert Team.objects.count() == teams_cnt
        assert Member.objects.count() == members_cnt
        data = response.json()
        members = data['team']['members']
        assert len(members) == 2
        assert 'full_name' in members[1]


@pytest.mark.django_db()
class TestUserAPI:

    def test_details(self, success_registration_data, quests):
        response = APIClient().post(
            reverse('registration'),
            data=success_registration_data,
            format='json',
        )

        assert response.status_code == 200
        registration_response_data = response.json()
        token = registration_response_data['token']
        user_id = registration_response_data['user']['id']

        team = Team.objects.first()
        coming_quest = quests[0]
        coming_quest_first_category = coming_quest.categories.first()
        coming_quest_first_category.teams.add(team)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.get(reverse('users-detail', args=[user_id]))
        assert response.status_code == 200
        users_response_data = response.json()

        # т.к. регистрация и юзеры делят общий сериалайзер отличаюзийся только рид онли
        # полями (идентификаторы и квесты), то здесь проверим только часть с квестами

        response_quests = users_response_data['team']['quests']
        assert len(response_quests) == 1  # команда зарегалась в одном квесте
        assert response_quests[0]['id'] == coming_quest.id
        assert len(response_quests[0]['categories']) == 1  # регистрация в одной из 5 категорий
        assert response_quests[0]['categories'][0]['id'] == coming_quest_first_category.id

        # теперь зарегистрируемся во втором квесте и проверим что данные изменились
        active_quest = quests[1]
        active_quest_first_category = active_quest.categories.first()
        active_quest_first_category.teams.add(team)

        response = client.get(reverse('users-detail', args=[user_id]))
        assert response.status_code == 200
        users_response_data = response.json()
        response_quests = users_response_data['team']['quests']
        assert len(response_quests) == 2
        assert response_quests[0]['id'] in (coming_quest.id, active_quest.id)
        assert response_quests[1]['id'] in (coming_quest.id, active_quest.id)
        assert response_quests[0]['id'] != response_quests[1]['id']
        assert len(response_quests[0]['categories']) == 1
        assert len(response_quests[1]['categories']) == 1

    def test_list(self, success_registration_data, success_registration_another_data, quests):
        client = APIClient()
        response = client.post(
            reverse('registration'),
            data=success_registration_data,
            format='json',
        )
        assert response.status_code == 200
        token = response.json()['token']

        response = client.post(
            reverse('registration'),
            data=success_registration_another_data,
            format='json',
        )
        assert response.status_code == 200

        registered_quests_ids = set()
        for team in Team.objects.all():
            for quest in quests:
                registered_quests_ids.add(quest.id)
                quest.categories.first().teams.add(team)

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.get(reverse('users-list'))
        assert response.status_code == 200
        users_response_data = response.json()['results']

        assert len(users_response_data) == 2
        for user in users_response_data:
            user_response_quests = user['team']['quests']
            assert len(user_response_quests) == 2
            assert user_response_quests[0]['id'] in registered_quests_ids
            assert user_response_quests[1]['id'] in registered_quests_ids
            assert user_response_quests[0]['id'] != user_response_quests[1]['id']
            assert len(user_response_quests[0]['categories']) == 1
            assert len(user_response_quests[1]['categories']) == 1

    def test_wrong_token(self):
        token = 'asasfadsfsd23423nj3nj3&%jhGJH7y'  # noqa: S105
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.get(reverse('users-list'))
        assert response.status_code == 401
        assert response.json()['detail'] == 'Invalid token.'
        response = client.get(reverse('users-detail', args=[1]))
        assert response.status_code == 401
        assert response.json()['detail'] == 'Invalid token.'

    def test_no_token(self):
        response = APIClient().get(reverse('users-list'))
        assert response.status_code == 401
        assert response.json()['detail'] == 'Authentication credentials were not provided.'
        response = APIClient().get(reverse('users-detail', args=[1]))
        assert response.status_code == 401
        assert response.json()['detail'] == 'Authentication credentials were not provided.'
