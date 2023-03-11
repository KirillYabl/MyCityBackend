from django.contrib.auth.hashers import check_password
from knox.models import AuthToken
from rest_framework import generics, permissions
from rest_framework.response import Response

from my_city.settings import TOKEN_INDEX

from .models import User
from .serializers import (CreateUserSerializer, LoginUserSerializer,
                          UserSerializer)


class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[TOKEN_INDEX]
        })


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=serializer.data['email'])
        if check_password(request.POST['password'], user.password):
            return Response({
            "token": AuthToken.objects.create(user)[TOKEN_INDEX]
            })
        else:
            return Response('Неверный пароль!')

class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
