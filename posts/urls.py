from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path(r'article_index/', views.ArticleListView.as_view(), name='article_index'),
    path(r'digital_file/', views.DigitalFileView.as_view(), name='digital_file'),
]