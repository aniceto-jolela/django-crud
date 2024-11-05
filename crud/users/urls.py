from django.urls import path
from . import views
from .views import (
    UserUpdateView,
    UserDetailView
)

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('users/', views.users, name='users'),
    path('user/<int:pk>/update/', UserUpdateView.as_view(), name='update')
]
