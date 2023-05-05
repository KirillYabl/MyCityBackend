from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, viewsets

from .filters import QuestFilter
from .models import Category, Quest, FAQ
from .serializers import CategorySerializer, QuestSerializer, FAQSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary="Список доступных квестов",
    operation_description="""Доступен для всех.
    Подключена LimitOffset пэджинация.
    Квесты будут отображаться только те,
    на которые уже началась регистрация или которые еще можно показывать.
    Есть также фильтрация по статусу.""",
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary="Получить квест по id",
    operation_description="""Доступен для всех.
    Доступные квеста как для списка
    (т.е. не получится получить квест, на который еще не началась регистрация)""",
))
class QuestAPI(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny ]
    serializer_class = QuestSerializer
    queryset = Quest.objects.which_show().with_status()
    filterset_class = QuestFilter


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary="Список категорий квеста",
    operation_description="""Доступен для всех.""",
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary="Получить одну из категорий квеста по id",
    operation_description="""Доступен для всех.""",
))
class CategoryAPI(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny ]
    serializer_class = CategorySerializer
    pagination_class = None

    def get_queryset(self):
        return Category.objects.filter(quest=self.kwargs['quest_pk'])


class FAQAPI(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny ]
    serializer_class = FAQSerializer
    pagination_class = None

    def get_queryset(self):
        return FAQ.objects.filter(question=self.kwargs['question_pk'])



