from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path(r'register/', views.RegisterView.as_view(success_url='/'), name='register'),
    path(r'login/', views.LoginView.as_view(success_url='/'), name='login'),
]