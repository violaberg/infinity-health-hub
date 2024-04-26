from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.article_list, name='articles'),
    path('articles/create/', views.create_article, name='create_article'),
    path('articles/<int:article_id>/',
         views.article_detail, name='article_detail'),
    path('articles/<int:article_id>/update/',
         views.update_article, name='update_article'),
    path('articles/<int:article_id>/delete/',
         views.delete_article, name='delete_article'),
    path('posts/', views.post_list, name='posts'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('posts/create/', views.create_post, name='create_post'),
    path('posts/<int:post_id>/like/', views.like_post, name='like_post'),
    path('posts/<int:post_id>/save/', views.save_post, name='save_post'),
]
