from django.urls import path
from . import api_views

app_name = 'api_auth'

urlpatterns = [
    path('api/sign-in', api_views.LoginAPIView.as_view()),
    path('api/sign-up', api_views.RegisterAPIView.as_view()),
    path('api/sign-out', api_views.LogoutAPIView.as_view()),
    path('api/profile', api_views.ProfileAPIView.as_view()),
    path('api/profile/password', api_views.PasswordChangeAPIView.as_view()),
    path('api/profile/avatar', api_views.AvatarChangeAPIView.as_view()),
]
