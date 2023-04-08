from django.urls import path
from knox import views as knox_views

from .views import RegistrationAPI, UserAPI

urlpatterns = [
    path('register/', RegistrationAPI.as_view(), name='registration'),
    path('login/', knox_views.LoginView.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('user/', UserAPI.as_view(), name='users'),
]
