import pytest
from django.utils import timezone

from user_app.models import User, Member, Team
from user_app.serializers import UserSerializer, TeamSerializer, MemberSerializer, CreateUserSerializer


@pytest.mark.django_db
class TestUserSerializer:
    def test_user_serializer(self):
        email = 'test@mail.ru'
        user = User.objects.create_user(email, 'sd#f35DGD3!d$%')
        serializer = UserSerializer(user)
        data = serializer.data
        assert data['id'] == user.id
        assert data['email'] == email


@pytest.mark.django_db
class TestTeamSerializer:
    def test_team_serializer(self):
        team_name = 'team1'
        user = User.objects.create_user('test@mail.ru', 'sd#f35DGD3!d$%')
        team = Team.objects.create(name=team_name, captain=user)
        serializer = TeamSerializer(team)
        data = serializer.data
        assert data['id'] == team.id
        assert data['name'] == team_name


@pytest.mark.django_db
class TestMemberSerializer:
    def test_member_serializer(self):
        user = User.objects.create_user('test@mail.ru', 'sd#f35DGD3!d$%')
        team = Team.objects.create(name='team1', captain=user)
        full_name = 'Иванов Иван'
        birth_date = '2016-09-17'
        phone = '+79054980738'
        email = 'test@mail.ru'
        is_captain = True
        member_number = 1
        member = Member.objects.create(
            full_name=full_name,
            birth_date=birth_date,
            phone=phone,
            email=email,
            is_captain=is_captain,
            member_number=member_number,
            team=team,
        )
        serializer = MemberSerializer(member)
        data = serializer.data
        assert data['id'] == member.id
        assert data['full_name'] == full_name
        assert data['birth_date'] == birth_date
        assert data['phone'] == phone
        assert data['email'] == email
        assert data['is_captain'] == is_captain
        assert data['member_number'] == member_number


@pytest.mark.django_db
class TestCreateUserSerializer:
    def test_create_user_serializer(self):
        data = {
            "email": "vasya@mail.ru",
            "password": "asd@$124Dsfd2",
            "team": {
                "name": "teamsdfkjskjsgb"
            },
            "members": [
                {
                    "full_name": "Василий Петрович",
                    "birth_date": "1978-02-15",
                    "phone": "+79003457896",
                    "email": "vasya@mail.ru",
                    "is_captain": True,
                    "member_number": 1
                },
                {
                    "full_name": "Иван Григорьевич",
                    "birth_date": "1975-02-15",
                    "phone": "+79003452896",
                    "email": "vasaya@mail.ru",
                    "is_captain": False,
                    "member_number": 2
                }
            ]
        }

        serializer = CreateUserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        assert serializer.data['email'] == "vasya@mail.ru"
        assert serializer.data['team']['name'] == "teamsdfkjskjsgb"
        assert len(serializer.data['members']) == 2
