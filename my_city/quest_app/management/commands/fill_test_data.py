import os
import random

from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from faker import Faker
from django.utils import timezone
from quest_app.models import (
    ContactType,
    Contact,
    FAQ,
    Quest,
    Category,
    AnswerType,
    Assignment,
    AnswerAttempt,
)
from user_app.models import (
    User,
    Team,
    Member,
)


class Command(BaseCommand):
    help = 'Заполняет тестовую БД фейковыми данными'

    @atomic
    def handle(self, *args, **options):
        fake_us = Faker()
        fake_ru = Faker(['ru-RU'])

        # Создание пользователей, команд и участников
        users = []
        teams = []
        members = []
        for user_i in range(100):
            email = fake_us.unique.email()
            password = fake_us.unique.password()
            user = User.objects.create_user(email='TEST_' + email, password=password)
            users.append(user)

            team_name = fake_ru.unique.word()
            team = Team.objects.create(name=team_name, captain=user)
            teams.append(team)

            for member_i in range(random.randint(2, 5)):
                is_captain = False
                if member_i == 0:
                    is_captain = True

                phone = ''
                email = ''
                if member_i in (0, 1):
                    phone = fake_ru.unique.phone_number()
                    email = fake_us.unique.email()

                member = Member.objects.create(
                    full_name=fake_ru.unique.name(),
                    is_captain=is_captain,
                    birth_date=fake_ru.date_of_birth(minimum_age=10, maximum_age=70),
                    phone=phone,
                    email=email,
                    member_number=member_i + 1,
                    team=team,
                )
                members.append(member)

        # Создание типов контактов и контактов
        contact_types = []
        for _ in range(2):
            name = fake_ru.word()
            contact_type = ContactType.objects.create(name='TEST_' + name)
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
            FAQ.objects.create(question='TEST_' + question, answer=answer, order=faq_i + 1)

        # Создание квестов
        now = timezone.now()
        quests = [
            Quest.objects.create(
                name='TEST_Open',
                description=fake_ru.paragraph(),
                registration_start_at=now - timezone.timedelta(days=1),
                start_at=now + timezone.timedelta(days=1),
                end_at=now + timezone.timedelta(days=2),
                stop_show_at=now + timezone.timedelta(days=3),
                address=fake_ru.address(),
                banner=os.path.join(Quest.banner.field.upload_to, 'default_picture.png'),
            ),
            Quest.objects.create(
                name='TEST_Active',
                description=fake_ru.paragraph(),
                registration_start_at=now - timezone.timedelta(days=2),
                start_at=now - timezone.timedelta(days=1),
                end_at=now + timezone.timedelta(days=1),
                stop_show_at=now + timezone.timedelta(days=2),
                address=fake_ru.address(),
                banner=os.path.join(Quest.banner.field.upload_to, 'default_picture.png'),
            ),
            Quest.objects.create(
                name='TEST_Finished with stop',
                description=fake_ru.paragraph(),
                registration_start_at=now - timezone.timedelta(days=3),
                start_at=now - timezone.timedelta(days=2),
                end_at=now - timezone.timedelta(days=1),
                stop_show_at=now + timezone.timedelta(days=1),
                address=fake_ru.address(),
                banner=os.path.join(Quest.banner.field.upload_to, 'default_picture.png'),
            ),
            Quest.objects.create(
                name='TEST_Finished no stop',
                description=fake_ru.paragraph(),
                registration_start_at=now - timezone.timedelta(days=3),
                start_at=now - timezone.timedelta(days=2),
                end_at=now - timezone.timedelta(days=1),
                address=fake_ru.address(),
                banner=os.path.join(Quest.banner.field.upload_to, 'default_picture.png'),
            )
        ]

        # Создание типов ответов
        answer_types = [
            AnswerType.objects.create(name='String'),
            AnswerType.objects.create(name='Numeric'),
            AnswerType.objects.create(name='Date'),
        ]

        # Создание категорий
        categories = []
        for quest in quests:
            teams_for_quest = random.sample(teams, k=50)
            for category_i in range(5):
                teams_for_category = teams_for_quest[category_i * 10:category_i * 10 + 10]
                name = fake_ru.word()
                category = Category.objects.create(
                    name=name,
                    quest=quest,
                    short_description=fake_ru.sentence(),
                    long_description=fake_ru.paragraph(),
                    participation_order=category_i + 1,
                    results_order=5 - category_i
                )
                for team in teams_for_category:
                    category.teams.add(team)
                category.save()
                categories.append(category)

                # TODO: для тестирования вопросов сделать более сложно
                if quest == quests[0]:
                    continue

                category_assignments = []
                for assignment_i in range(15):
                    assignment = Assignment.objects.create(
                        category=category,
                        answer_type=random.choice(answer_types),
                        picture=os.path.join(Quest.banner.field.upload_to, 'default_picture.png'),
                        question=fake_ru.sentence(),
                        answer=fake_ru.word(),
                        is_enumeration=False,
                    )
                    category_assignments.append(assignment)

                for team in teams_for_category:
                    answers_count = random.randint(0, 15)
                    team_category_assignments = random.sample(category_assignments, k=answers_count)
                    for assignment in team_category_assignments:
                        AnswerAttempt.objects.create(
                            assignment=assignment,
                            team=team,
                            answer=fake_ru.word(),
                            auto_result=random.randint(0, 100) > 50,
                            prevent_result=random.randint(0, 100) > 5,
                            not_sure=random.randint(0, 100) > 10,
                        )

        self.stdout.write(self.style.SUCCESS('Данные успешно созданы'))
