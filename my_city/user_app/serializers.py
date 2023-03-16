from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from rest_framework import serializers

from .models import User


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['email'],
                                        validated_data['password'])
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email')



class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate_password(self, request):
        email = request.get('email')
        password = request.get('password')
        user = authenticate(email=email, password=password)
        if check_password(user.password, password):
            return password

