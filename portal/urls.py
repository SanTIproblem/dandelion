from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'portal'

urlpatterns = [
    path(r'', views.open_home_page, name='home'),

]