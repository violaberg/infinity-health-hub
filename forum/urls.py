from django.urls import path
from . import views

urlpatterns = [
    path('', views.forum, name='forum'),
    path('articles/', views.article_list, name='articles'),
    path('posts/', views.post_list, name='posts'),
    path('articles/<slug:slug>', views.article_detail, name='article_detail'),
    path('posts/<slug:slug>', views.post_detail, name='post_detail'),

]