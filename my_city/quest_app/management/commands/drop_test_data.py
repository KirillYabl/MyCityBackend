from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from user_app.models import Member, Team, User

from quest_app.models import (
    FAQ,
    AnswerAttempt,
    AnswerType,
    Assignment,
    Category,
    Contact,
    ContactType,
    Quest,
)


class Command(BaseCommand):
    """Заполняет тестовую БД фейковыми данными"""

    @atomic
    def handle(self, *args, **options):  # noqa: ARG002
        test_quest_ids = [quest.id for quest in Quest.objects.filter(name__contains='TEST')]
        test_answer_type_ids = {
            assignment.answer_type.id
            for assignment in Assignment.objects.filter(category__quest__id__in=test_quest_ids)
        }
        test_user_ids = [user.id for user in User.objects.filter(email__contains='TEST_')]
        AnswerAttempt.objects.filter(assignment__category__quest__id__in=test_quest_ids).delete()
        Assignment.objects.filter(category__quest__id__in=test_quest_ids).delete()
        Category.objects.filter(quest__id__in=test_quest_ids).delete()
        Quest.objects.filter(id__in=test_quest_ids).delete()
        AnswerType.objects.filter(id__in=test_answer_type_ids).delete()
        FAQ.objects.filter(question__contains='TEST').delete()
        Contact.objects.filter(contact_type__name__contains='TEST').delete()
        ContactType.objects.filter(name__contains='TEST').delete()
        Member.objects.filter(team__captain__id__in=test_user_ids).delete()
        Team.objects.filter(captain__id__in=test_user_ids).delete()
        User.objects.filter(id__in=test_user_ids).delete()

        self.stdout.write(self.style.SUCCESS('Данные успешно удалены'))
