import json

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from .models import Profile, Avatar
from django.contrib.auth import login, logout, authenticate
from .serializers import UserRegisterSerializer, ProfileSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response


class LoginAPIView(APIView):

    def post(self, request: Request):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutAPIView(APIView):

    def post(self, request):
        user = request.user
        logout(request)
        if user is not None:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RegisterAPIView(APIView):

    def post(self, request):
        data = json.loads(request.body)
        serializer = UserRegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save(request)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProfileAPIView(APIView):

    def get(self, request):
        user = Profile.objects.get(user_id=request.user.pk)
        serializer = ProfileSerializer(user)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        full_name = data.get('fullName')
        phone = data.get('phone')
        email = data.get('email')
        Profile.objects.filter(user_id=request.user.pk).update(
            fullName=full_name,
            phone=phone,
            second_email=email,
        )
        user_profile = Profile.objects.get(user_id=request.user.pk)
        serializer = ProfileSerializer(user_profile)
        return Response(serializer.data)


class PasswordChangeAPIView(APIView):

    def post(self, request):
        data = request.data
        current_password = data.get('currentPassword')
        new_password = data.get('newPassword')
        user = User.objects.get(pk=request.user.pk)
        if user.check_password(current_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class AvatarChangeAPIView(APIView):

    def post(self, request):
        avatar = request.FILES['avatar']
        print('*******************************************************')
        print('Блок до if')
        if avatar:
            if Avatar.objects.filter(user_id=request.user.pk).exists():
                print('*******************************************************')
                print(Avatar.objects.filter(user_id=request.user.pk).exists())
                user_avatar = Avatar.objects.get(user_id=request.user.pk)
                user_avatar.src = avatar
                user_avatar.save()
                return Response(status=status.HTTP_200_OK)
            else:
                print('*******************************************************')
                print('Попал в создание объекта')
                profile = Profile.objects.get(user_id=request.user.pk)
                print(profile)
                Avatar.objects.create(
                    user_id=profile.user_id,
                    src=avatar,
                )
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
