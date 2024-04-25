from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.article_list, name='articles'),
    path('posts/', views.post_list, name='posts'),
    path('articles/<slug:slug>', views.article_detail, name='article_detail'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('posts/create/', views.create_post, name='create_post'),
]