"""Теперь напиши пожалуйста менеджемент команду для django, которая умеет
1. Заполнять тестовую БД фуковыми данными, с помощью библиотеки Faker
2. Удалять ранее заполненную БД (только тестовые данные удаляются)
3. Обновлять БД (объединение второй и первой операции в одну)

Количество фейковых записей по таблицам:
    User - 100
    Team - 100 (по 1 для каждого юзера)
    Member - по 2-5 на каждую команду (у 2 игроков (капитан и второй игрок) обязательно должны быть заполнены телефоны и email, у остальных не обязательно, обязательно в команде есть капитан). Тут же создавай связь в таблице TeamMembership, у капитана первый номер, у второго учатсника второй и так далее.
    ContactType - 2
    Contact - 5
    FAQ- 7
    Quest - 3
Активный квест - start_at < now < end_at
Прошедщий квест - end_at < now < stop_show_at
Прошедщий квест - end_at < now < stop_show_at
причем registration_start_at < start_at < end_at < stop_show_at
    Category - 15 (по 5 в каждом квесте). Когда создаешь категорию, добавляй в нее команду по следующим ограничениям: одна команда участвует только в одной случайно категории из квеста, которому принадлежат категории, команда может вообще не участвовать ни в одной категори квеста. Сделай так, что бы в каждом квесте участвовало около половины команд.
    AnswerType - 3 (строковый, числовой и дата)
    Assignment - 225 (по 15 в каждой категории)
    AnswerAttempt - от 10 до 100 для каждого Assignment (одна команда может давать только 1 ответ на один задание, но может и не давать). Ответ на задание могут давать только те команды, которые участвуют в категори, которой принаджежит задание
"""
import random

from django.core.management.base import BaseCommand
from faker import Faker
from random import randint
from datetime import datetime, timedelta
from django.utils import timezone
from myapp.models import User, Team, Member, ContactType, Contact, FAQ, Quest, Category, AnswerType, Assignment, \
    AnswerAttempt, TeamMembership


class Command(BaseCommand):
    help = 'Заполняет тестовую БД фейковыми данными'

    def handle(self, *args, **options):
        fake_us = Faker()
        fake_ru = Faker(['ru-RU'])

        # Создание пользователей, команд и участников
        users = []
        teams = []
        members = []
        team_memberships = []
        for user_i in range(100):
            email = fake_us.unique.email()
            password = fake_us.unique.password()
            user = User.objects.create_user(email=email, password=password)
            users.append(user)

            team_name = fake_ru.unique.word()
            team = Team.objects.create(name=team_name, captain=user)
            teams.append(team)

            for member_i in range(randint(2, 5)):
                is_captain = False
                if member_i == 0:
                    is_captain = True
                member = Member.objects.create(full_name=fake_us.unique.name(), team=team, is_captain=is_captain)
                members.append(member)
                team_membership = TeamMembership.objects.create(team=team, member=member, number=member_i + 1)
                team_memberships.append(team_membership)

        # Создание типов контактов и контактов
        contact_types = []
        for _ in range(2):
            name = fake_ru.word()
            contact_type = ContactType.objects.create(name=name)
            contact_types.append(contact_type)

        for contact_i in range(5):
            contact_type = random.choice(contact_types)
            contact = fake_ru.unique.phone_number()
            description = fake_ru.sentence()
            Contact.objects.create(
                contact_type=contact_type,
                contact=contact,
                description=description,
                order=contact_i + 1
            )

        # Создание FAQ
        for faq_i in range(7):
            question = fake_ru.sentence()
            answer = fake_ru.paragraph()
            FAQ.objects.create(question=question, answer=answer, order=faq_i + 1)

        # Создание квестов
        quests = [
            Quest.objects.create(
                name='Open',
                description=fake_ru.paragraph(),
                registration_start_at=fake_us.date_time_this_year(before_now=True, after_now=False),
                start_at=fake_us.date_time_this_year(before_now=False, after_now=True),
                end_at=fake_us.date_time_this_year(before_now=False, after_now=True),
                stop_show_at=fake_us.date_time_this_year(before_now=False, after_now=True),
                address=fake_ru.address(),
            ),
            Quest.objects.create(
                name='Active',
                description=fake_ru.paragraph(),
                registration_start_at=fake_us.date_time_this_year(before_now=True, after_now=False),
                start_at=fake_us.date_time_this_year(before_now=True, after_now=False),
                end_at=fake_us.date_time_this_year(before_now=False, after_now=True),
                stop_show_at=fake_us.date_time_this_year(before_now=False, after_now=True),
                address=fake_ru.address(),
            ),
            Quest.objects.create(
                name='Finished with stop',
                description=fake_ru.paragraph(),
                registration_start_at=fake_us.date_time_this_year(before_now=True, after_now=False),
                start_at=fake_us.date_time_this_year(before_now=True, after_now=False),
                end_at=fake_us.date_time_this_year(before_now=False, after_now=True),
                stop_show_at=fake_us.date_time_this_year(before_now=False, after_now=True),
                address=fake_ru.address(),
            ),
            Quest.objects.create(
                name='Finished no stop',
                description=fake_ru.paragraph(),
                registration_start_at=fake_us.date_time_this_year(before_now=True, after_now=False),
                start_at=fake_us.date_time_this_year(before_now=True, after_now=False),
                end_at=fake_us.date_time_this_year(before_now=False, after_now=True),
                address=fake_ru.address(),
            )
        ]

        # Создание категорий
        categories = []
        for quest in quests:
            for i in range(5):
                name = fake_ru.word()
                category = Category.objects.create(name=name, quest=quest)
                categories.append(category)

            # Создание типов ответов
            answer_types = [
                AnswerType.objects.create(name='String'),
                AnswerType.objects.create(name='Numeric'),
                AnswerType.objects.create(name='Date'),
            ]

            # Создание заданий и попыток ответов
            assignments = []
            answer_attempts = []
            for category in categories:
                for i in range(randint(2, 5)):
                    assignment = Assignment.objects.create(category=category, text=fake.text())
                    assignments.append(assignment)
                    for member in category.quest.team.members.all():
                        attempt = AnswerAttempt.objects.create(assignment=assignment, member=member,
                                                               answer_type=AnswerType.objects.first())
                        answer_attempts.append(attempt)

            self.stdout.write(self.style.SUCCESS('Данные успешно созданы'))
