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
        assert Member.objects.count() == members_cnt + len(success_registration_data['members'])
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
        assert 'This field may not be blank.' in data['email']
        assert 'This field may not be blank.' in data['password']
        assert 'This field may not be blank.' in data['team']['name']
        assert 'This field is required.' in data['members'][0]['full_name']
        assert 'This field is required.' in data['members'][0]['birth_date']
        assert 'This field is required.' in data['members'][0]['is_captain']
        assert 'This field is required.' in data['members'][0]['member_number']

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
        assert 'Enter a valid email address.' in data['email']
        assert 'Ensure this field has at least 8 characters.' in data['password']
        assert 'name' in data['team']
        assert len(data['members']) == 2
        assert 'full_name' in data['members'][0]
        assert 'birth_date' in data['members'][0]
        assert 'phone' in data['members'][0]
        assert 'is_captain' in data['members'][0]
        assert 'member_number' in data['members'][0]
        assert 'full_name' in data['members'][1]
        assert 'phone' in data['members'][1]
        assert 'email' in data['members'][1]
        assert 'member_number' in data['members'][1]

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
        assert len(data['members']) == 4
        assert 'is_captain' in data['members'][0]
        assert 'phone' in data['members'][0]
        assert 'phone' in data['members'][1]
        assert 'email' in data['members'][1]
        assert 'is_captain' in data['members'][2]
        assert 'full_name' in data['members'][2]
        assert 'full_name' in data['members'][3]

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
        members_cnt += len(success_registration_data['members'])
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
        assert len(data['members']) == 2
        assert 'full_name' in data['members'][1]


@pytest.mark.django_db()
class TestUserAPI:
    """The main tests purpose is check auth by token because it's only api in app"""

    def test_success(self, success_registration_data):
        response = APIClient().post(
            reverse('registration'), data=success_registration_data, format='json',
        )
        assert response.status_code == 200
        token = response.json()['token']

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.get(reverse('users'))
        assert response.status_code == 200

    def test_wrong_token(self):
        token = 'asasfadsfsd23423nj3nj3&%jhGJH7y'  # noqa: S105
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.get(reverse('users'))
        assert response.status_code == 401
        assert response.json()['detail'] == 'Invalid token.'

    def test_no_token(self):
        response = APIClient().get(reverse('users'))
        assert response.status_code == 401
        assert response.json()['detail'] == 'Authentication credentials were not provided.'
