from django.urls import path, include
from rest_framework_nested import routers

from .views import QuestAPI, CategoryAPI, FAQAPI

router = routers.SimpleRouter()
router.register(r'quests', QuestAPI)

quest_category_router = routers.NestedSimpleRouter(router, r'quests', lookup='quest')
quest_category_router.register(r'categories', CategoryAPI, basename='quest-categories')

faqs_router = routers.SimpleRouter()
faqs_router.register(r'faqs', FAQAPI, basename='FAQ')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(quest_category_router.urls)),
]
