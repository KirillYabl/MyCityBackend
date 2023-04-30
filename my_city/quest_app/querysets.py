from django.db import models
from django.db.models import Q
from django.utils import timezone

from .choices import QuestStatus


class QuestQueryset(models.QuerySet):
    def which_show(self):
        """Показывать только те, у которых регистрация уже началась и их еще можно показывать."""
        return self.filter(
            Q(stop_show_at__isnull=True) | Q(stop_show_at__gt=timezone.now()),
            registration_start_at__lte=timezone.now(),
        )

    def with_status(self):
        """Подтянуть статус квеста.

        Вычисляемое поле, нет смысла хранить в БД.
        """
        now = timezone.now()
        return self.annotate(
            status=models.Case(
                models.When(
                    registration_start_at__lte=now,
                    start_at__gt=now,
                    then=models.Value(QuestStatus.coming),
                ),
                models.When(
                    start_at__lte=now,
                    end_at__gt=now,
                    then=models.Value(QuestStatus.active),
                ),
                models.When(
                    Q(stop_show_at__isnull=True) | Q(stop_show_at__gt=now),
                    end_at__lte=now,
                    then=models.Value(QuestStatus.finished),
                ),
            ),
        )
