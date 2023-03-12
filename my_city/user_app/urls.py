from django.urls import path
from knox import views as knox_views

from .views import LoginAPI, RegistrationAPI, UserAPI

urlpatterns = [
    path('register/', RegistrationAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('user/', UserAPI.as_view()),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
]
