from django.urls import path
from . import views
from .views import (
    UserUpdateView,
    UserDetailView,
    UserDeleteView,
    UserListView
)


urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('users/', UserListView.as_view(), name='users'),
    path('user/<int:pk>/update/', UserUpdateView.as_view(), name='update'),
    path('user/new/', views.register, name='register'),
    path('user/<int:pk>/detail/', UserDetailView.as_view(), name='detail'),
    path('user/<int:pk>/delete/', UserDeleteView.as_view(), name='delete'),
    path('user/<int:pk>/update_pic/', views.update_pic, name='update_pic'),
    path('user/register_photo/', views.register_photo_with_user, name='register_photo'),
    path('management/', views.management, name='management'),
    path('delete_all_data/', views.delete_all_data, name='delete_all_data'),
    path('login/', views.UserLoginView.as_view(), name='login'),
]
