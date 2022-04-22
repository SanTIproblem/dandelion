from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'comments'

urlpatterns = [
    path(r'article/<int:article_id>/post_comment', views.CommentsView.as_view(),name='post_comment')
]