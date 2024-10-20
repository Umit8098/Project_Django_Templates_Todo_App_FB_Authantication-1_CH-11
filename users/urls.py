from django.urls import path, include
from .views import (
    register,
    user_login,
)
from django.contrib.auth.views import LogoutView

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='user_login'),

    # custom password_chage view and template
    path('logouts/', LogoutView.as_view(), name='user_logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name="registration/password_change.html"), name="password_change"),
]
