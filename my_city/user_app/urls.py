from django.urls import include, path
from knox import views as knox_views
from rest_framework_nested import routers

from .views import RegistrationAPI, UserAPI

router = routers.SimpleRouter()
router.register('', UserAPI, basename='users')

urlpatterns = [
    path('register/', RegistrationAPI.as_view(), name='registration'),
    path('login/', knox_views.LoginView.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('', include(router.urls)),
]
