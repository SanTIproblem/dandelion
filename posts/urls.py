from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path(r'article_index/', views.IndexView.as_view(), name='article_index'),
    # path(r'digital_file/', views.DigitalFileView.as_view(), name='digital_file'),
    path(r'digital_file/', views.get_digital_file, name='digital_file'),
    path(r'edit_article/', views.EditArticleView.as_view(), name='edit_article'),
    path(r'article/<int:year>/<int:month>/<int:day>/<int:article_id>.html',
         views.ArticleDetailView.as_view(),name='get_detail_by_id')
]