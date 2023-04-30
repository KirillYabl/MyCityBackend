from django.urls import include, path
from rest_framework_nested import routers

from .views import CategoryAPI, QuestAPI

router = routers.SimpleRouter()
router.register(r'quests', QuestAPI)

quest_category_router = routers.NestedSimpleRouter(router, r'quests', lookup='quest')
quest_category_router.register(r'categories', CategoryAPI, basename='quest-categories')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(quest_category_router.urls)),
]
