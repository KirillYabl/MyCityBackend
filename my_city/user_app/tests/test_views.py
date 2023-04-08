import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from knox.models import AuthToken
from knox.crypto import hash_token

from user_app.models import User


@pytest.mark.django_db
class TestRegistrationAPI:
    def test_success(self):
        email = 'test_email@gmail.com'
        response_data = {
            'email': email,
            'password': 'J3@4asNFh31Df!'
        }
        users_cnt = User.objects.count()
        response = APIClient().post(reverse('registration'), data=response_data)
        assert response.status_code == 200
        assert User.objects.count() == users_cnt + 1
        new_user = User.objects.get(email=email)
        data = response.json()
        assert 'user' in data
        assert data['user']['email'] == new_user.email
        assert data['user']['id'] == new_user.id
        assert data['user']['email'] == email
        assert 'token' in data
        AuthToken.objects.get(user=new_user, digest=hash_token(data['token']))

    def test_invalid_email(self):
        email = 'test'
        response_data = {
            'email': email,
            'password': 'J3@4asNFh31Df!'
        }
        users_cnt = User.objects.count()
        response = APIClient().post(reverse('registration'), data=response_data)
        assert response.status_code == 400
        data = response.json()
        assert User.objects.count() == users_cnt
        assert 'Enter a valid email address.' in data['email']

    def test_invalid_password(self):
        email = 'test_email@gmail.com'
        passwords = ['asQ1@', '12345678']
        error_messages = [
            'Ensure this field has at least 8 characters.',
            'This password is too common.',
        ]
        for password, error_message in zip(passwords, error_messages):
            response_data = {
                'email': email,
                'password': password,
            }
            users_cnt = User.objects.count()
            response = APIClient().post(reverse('registration'), data=response_data)
            assert response.status_code == 400
            data = response.json()
            assert User.objects.count() == users_cnt
            assert 'password' in data
            assert error_message in data['password']

    def test_repeat_email(self):
        email = 'test_email@gmail.com'
        response_data = {
            'email': email,
            'password': 'J3@4asNFh31Df!'
        }
        users_cnt = User.objects.count()
        response = APIClient().post(reverse('registration'), data=response_data)
        assert response.status_code == 200
        users_cnt += 1
        assert User.objects.count() == users_cnt
        response = APIClient().post(reverse('registration'), data=response_data)
        data = response.json()
        assert response.status_code == 400
        assert User.objects.count() == users_cnt
        assert 'email' in data
        assert 'пользователь with this email address already exists.' in data['email']


@pytest.mark.django_db
class TestUserAPI:
    """The main tests purpose is check auth by token because it's only api in app"""
    def test_success(self):
        email = 'test_email@gmail.com'
        response_data = {
            'email': email,
            'password': 'J3@4asNFh31Df!'
        }
        response = APIClient().post(reverse('registration'), data=response_data)
        assert response.status_code == 200
        token = response.json()['token']

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.get(reverse('users'))
        assert response.status_code == 200

    def test_wrong_token(self):
        token = 'asasfadsfsd23423nj3nj3&%jhGJH7y'
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.get(reverse('users'))
        assert response.status_code == 401
        assert 'Invalid token.' == response.json()['detail']

    def test_no_token(self):
        response = APIClient().get(reverse('users'))
        assert response.status_code == 401
        assert 'Authentication credentials were not provided.' == response.json()['detail']

