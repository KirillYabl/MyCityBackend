from django.utils import timezone
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, viewsets

from .filters import QuestFilter
from .models import Quest
from .serializers import QuestSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary="Список доступных квестов",
    operation_description="""Доступен для всех.
    Подключена LimitOffset пэджинация.
    Квесты будут отображаться только те, на которые уже началась регистрация или которые еще можно показывать.
    Есть также фильтрация по статусу.""",
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary="Получить квест по id",
    operation_description="""Доступен для всех.
    Доступные квеста как для списка (т.е. не получится получить квест, на который еще не началась регистрация)""",
))
class QuestAPI(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = QuestSerializer
    queryset = Quest.objects.which_show().with_status()
    filterset_class = QuestFilter
