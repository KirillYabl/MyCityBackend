from django.shortcuts import get_object_or_404
from knox.models import AuthToken
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import User
from .serializers import (CreateUserSerializer, LoginUserSerializer,
                          UserSerializer)

token_index = 1


class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[token_index]
        })


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, email=serializer.data['email'])
        if serializer.is_valid():
            return Response({
            "token": AuthToken.objects.create(user)[token_index]
            })
        return Response('Неверный пароль!', status=status.HTTP_404_NOT_FOUND)

class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
