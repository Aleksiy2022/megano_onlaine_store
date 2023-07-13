from django.urls import path, include
from .api_views import (
    LoginAPIView,
    RegisterAPIView,
    LogoutAPIView,
    ProfileAPIView,
    PasswordChangeAPIView,
    AvatarChangeAPIView
)

app_name = 'api_auth'

urlpatterns = [
    path('api/sign-in', LoginAPIView.as_view()),
    path('api/sign-up', RegisterAPIView.as_view()),
    path('api/sign-out', LogoutAPIView.as_view()),
    path('api/profile', ProfileAPIView.as_view()),
    path('api/profile/password', PasswordChangeAPIView.as_view()),
    path('api/profile/avatar', AvatarChangeAPIView.as_view()),
]
