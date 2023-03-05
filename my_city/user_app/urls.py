from django.urls import path
from .views import RegistrationAPI,LoginAPI
from knox import views as knox_views

urlpatterns = [
     path(r'register/', RegistrationAPI.as_view(), name='knox_register'),
     path(r'login/', LoginAPI.as_view(), name='knox_login'),
     path('logout/', knox_views.LogoutView.as_view(), name='knox_logout')
]