import knox.auth
from django.contrib.auth import get_user_model
from knox.models import AuthToken
from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response

from .serializers import ComplexUserSerializer, UserSerializer

User = get_user_model()

token_index = 1


class RegistrationAPI(generics.GenericAPIView):
    """"Регистрация команды."""
    serializer_class = ComplexUserSerializer

    def post(self, request, *args, **kwargs) -> Response:  # noqa: ARG002
        """Регистрация команды.

        Состоит из трех этапов.

        1) Создание пользователя по почте и паролю
        Проверяется валидность почты и сложность пароля

        2) Создание команды для пользователя по имени
        Проверяется имя команды, проверки не сложные, по длине и много пробелов между словами
        запрещено, а также в начеле и конце пробелы запрещены

        3) Создание участников команды с капитаном
        Проверяется по каждому участнику:
        - Капитан один и под первым номером
        - Остальные не капитаны
        - У первых двух (настраиваемо) обязательных участников есть почта и номер телефона
        - В одной команде не повторяется комбинация имени и даты рождения

        Если будут ошибки в участниках, то они записываются примерно в таком виде, как передавались
        т.е. список из словарей, порядок тот же

        И в конце вся информация проверяется вместе,
        найденные тут ошибки записываются в поле `members_general`
        - почта пользователя и капитана совпадают
        - количество участников от 2 до 5
        - нет пропусков в номерах участников
        - почты всех участников уникальны
        - телефоны всех участников уникальны
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": AuthToken.objects.create(user)[token_index],
            },
        )


class UserAPI(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [knox.auth.TokenAuthentication ]
    permission_classes = [permissions.IsAuthenticated ]
    serializer_class = ComplexUserSerializer
    queryset = User.objects.prefetch_related(
        'team',
        'team__members',
        'team__categories',
        'team__categories__quest',
    )

