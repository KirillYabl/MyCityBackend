from django.contrib.auth import password_validation
from rest_framework import serializers
from django.core import exceptions

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

    def validate_password(self, password):
        # https://gist.github.com/leafsummer/f4d67b58a4cc77174c31935d7e299c9e
        try:
            password_validation.validate_password(password=password)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(list(e.messages))

        return password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email')
