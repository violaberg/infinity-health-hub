from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_profile, name='profile'),
#    path('<int:profile_id>/', views.profile_detail, name='profile_detail')
]
