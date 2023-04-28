import collections
from collections import defaultdict

from django.contrib.auth import password_validation, get_user_model
from django.conf import settings
from django.core import exceptions
from django.db.transaction import atomic
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Team, Member
from quest_app.models import Quest
from quest_app.serializers import QuestCategoriesSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email')


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = (
            'id',
            'full_name',
            'birth_date',
            'phone',
            'email',
            'is_captain',
            'member_number'
        )


class TeamSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True)
    quests = SerializerMethodField('get_quests', read_only=True)

    class Meta:
        model = Team
        fields = ('id', 'name', 'members', 'quests',)

    def get_quests(self, team):
        """
        Достать список квестов для команды.

        Но при этом категории у квеста оставить только те, в которых участвует команда

        Причина использования этого метода, вместо обычных вложенных сериализаторов следующая
        1. Для фронтенда и для заказчика понятие квеста более первичное, чем категории, потому что пользователь
        регистрируется на квест. Но со стороны архитектуры БД было правильнее сделать связь команды с квестом не
        напрямую, а через категорию
        2. Соответственно фронтенду удобнее получать в привязке к команде квесты, а не категории
        3. И еще у квеста есть кверисет с особыми методами, которые в других кверисетах соответственно
        не получится использовать

        этот метод для листа в худшем случае производит N*2 лищних запросов, где N количество записей
        но вообще апи юзеров с листом не должно часто вызываться
        первый лишний запрос при вызове сериалайзера внутри, сериалайзер по id ищет квест там
        второй лишний запрос при отборе категорий вручную, его в теории можно как-то
        сократить, но пока не понял как
        """

        # если сериализатор создается, то команда это не объект БД, а словарь и соответственно
        # еще нигде не участвует. И тогда нужно вернуть пустой список (почему она вообще вызывается при записи,
        # хотя установленно, что поле только для чтения я не разобрался, видимо баг в джанге)
        if type(team) == collections.OrderedDict:
            return []

        team_categories = team.categories.all()
        quests = set(category.quest for category in team_categories if category.quest.is_show())
        serialized_quests = QuestCategoriesSerializer(instance=quests, many=True).data
        team_categories_ids = team.categories.values_list('id', flat=True)

        # оставим только те категории, в которых участвует команда, с помощью ORM это не сделать :(
        for quest_index, quest in enumerate(serialized_quests):
            quest_categories = [category for category in quest['categories'] if category['id'] in team_categories_ids]
            serialized_quests[quest_index]['categories'] = quest_categories

        return serialized_quests

    def validate_members(self, members):
        error_messages = [{} for _ in members]
        captain_number = 1
        email_phone_required_numbers = list(range(1, settings.MIN_MEMBERS_IN_TEAM + 1))
        member_names_and_birthdates = set()
        for member_index, member in enumerate(members):
            member_errors = defaultdict(list)
            member_number = member['member_number']
            # проверим, что у первого участника есть признак капитана, а у остальных нет
            if member_number == captain_number and not member['is_captain']:
                member_errors['is_captain'].append('Первый участник должен быть капитаном')
            elif member_number != captain_number and member['is_captain']:
                member_errors['is_captain'].append('Только первый участник может быть капитаном')

            # проверим, что телефон и почта указаны у участников, у которых должны быть указаны
            check_email_phone = member_number in email_phone_required_numbers
            member_has_phone = 'phone' in member and len(member['phone']) > 0
            member_has_email = 'email' in member and len(member['email']) > 0

            if check_email_phone and not member_has_phone:
                member_errors['phone'].append('У данного члена команды должен быть указан телефон')
            if check_email_phone and not member_has_email:
                member_errors['email'].append(f'У данного члена команды должен быть указан email')

            # проверим, что имя с датой рождения не повторяются
            # имена еще возможны (вдруг отца и сына одинаково зовут)
            # но с датами рождения маловероятно, близнецов редко называют одинаково
            member_name_birthdate = (member['full_name'], member['birth_date'])
            if member_name_birthdate not in member_names_and_birthdates:
                member_names_and_birthdates.add(member_name_birthdate)
            else:
                name, birthdate = member_name_birthdate
                member_errors['full_name'].append(
                    f'{name} ({birthdate}) уже есть в команде под другим номером'
                )

            error_messages[member_index] = member_errors

        if [member_errors for member_errors in error_messages if member_errors]:
            raise serializers.ValidationError(error_messages, code='members_errors')

        return members


class ComplexUserSerializer(serializers.ModelSerializer):
    team = TeamSerializer()

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'team',)
        extra_kwargs = {
            'password': {'write_only': True},
        }

    @atomic
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['email'],
                                        validated_data['password'])
        team_data = validated_data.pop('team')
        members_data = team_data.pop('members')

        team = Team.objects.create(captain=user, **team_data)
        members = [
            Member(team=team, **member_data)
            for member_data
            in members_data
        ]
        Member.objects.bulk_create(members)
        return user

    def validate(self, attrs):
        error_messages = []
        email = attrs['email']
        members = attrs['team']['members']
        try:
            captain_email = sorted(members, key=lambda x: x['member_number'])[0]['email']
        except IndexError:
            captain_email = ''

        if email != captain_email:
            error_messages.append(
                exceptions.ValidationError(
                    'email для регистрации и у капитана должны совпадать',
                    code='wrong_captain_email'
                ),
            )

        # это проверки про members, но они здесь, потому что они не относятся к какому-то
        # конкретному участнику команды и должны иметь свой лейбл
        if len(members) < settings.MIN_MEMBERS_IN_TEAM or len(members) > settings.MAX_MEMBERS_IN_TEAM:
            error_messages.append(
                exceptions.ValidationError(
                    f'Число участников должно быть от {settings.MIN_MEMBERS_IN_TEAM} до {settings.MAX_MEMBERS_IN_TEAM}',
                    code='wrong_members_count'
                ),
            )

        member_numbers = [member['member_number'] for member in members]
        if set(member_numbers) != set(range(1, len(members) + 1)):
            error_messages.append(
                exceptions.ValidationError(
                    f'Между номерами участников не должно быть пропусков и повторов (от 1 до {len(members)})',
                    code='member_number_duplicate'
                ),
            )

        member_emails = [member.get('email', '') for member in members if member.get('email', '')]
        member_phones = [member.get('phone', '') for member in members if member.get('phone', '')]

        if len(set(member_emails)) != len(member_emails):
            error_messages.append(
                exceptions.ValidationError(
                    'У всех участников, у которых задан email, они должны быть разными',
                    code='email_duplicate'
                ),
            )

        if len(set(member_phones)) != len(member_phones):
            error_messages.append(
                exceptions.ValidationError(
                    'У всех участников, у которых задан телефон, они должны быть разными',
                    code='phone_duplicate'
                ),
            )

        if error_messages:
            raise exceptions.ValidationError({'members_general': error_messages}, code='members_general')

        return attrs

    def validate_password(self, password):
        # https://gist.github.com/leafsummer/f4d67b58a4cc77174c31935d7e299c9e
        try:
            password_validation.validate_password(password=password)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(list(e.messages), code='invalid_password')

        return password
