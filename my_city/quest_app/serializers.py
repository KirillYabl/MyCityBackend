from rest_framework import serializers

from .choices import QuestStatus
from .models import Category, Quest


class QuestSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=QuestStatus.choices)

    class Meta:
        model = Quest
        fields = (
            'id',
            'name',
            'description',
            'registration_start_at',
            'start_at',
            'end_at',
            'stop_show_at',
            'address',
            'banner',
            'status',
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'short_description',
            'long_description',
            'participation_order',
            'results_order',
        )


class QuestCategoriesSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=QuestStatus.choices)
    categories = CategorySerializer(many=True)

    class Meta:
        model = Quest
        fields = (
            'id',
            'name',
            'description',
            'registration_start_at',
            'start_at',
            'end_at',
            'stop_show_at',
            'address',
            'banner',
            'status',
            'categories',
        )
