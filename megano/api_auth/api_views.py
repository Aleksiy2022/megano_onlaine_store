import json
from cart.utils import merge_carts
from .models import Profile, Avatar
from django.contrib.auth import login, logout, authenticate
from .serializers import UserRegisterSerializer, ProfileSerializer, EmptySerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Auth'])
class LoginAPIView(APIView):
    """
    Аутентификация и авторизация пользователя.
    """

    serializer_class = EmptySerializer

    def post(self, request: Request)-> Response:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            merge_carts(request=request, user=user)
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(tags=['Auth'])
class LogoutAPIView(APIView):
    """
    Выход из системы пользователя.
    """

    serializer_class = EmptySerializer

    def post(self, request: Request) -> Response:
        logout(request)
        user = request.user
        if user is not None:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(tags=['Auth'])
class RegisterAPIView(APIView):
    """
    Регистрация нового пользователя.
    """

    serializer_class = EmptySerializer

    def post(self, request: Request) -> Response:
        data = json.loads(request.body)
        serializer = UserRegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save(request)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(tags=['Auth'])
class ProfileAPIView(APIView):
    """
    Получение и обновление данных пользователя.
    """

    serializer_class = ProfileSerializer

    def get(self, request: Request) -> Response:
        user = Profile.objects.select_related('avatar').get(user_id=request.user.pk)
        serializer = ProfileSerializer(user)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
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


@extend_schema(tags=['Auth'])
class PasswordChangeAPIView(APIView):
    """
    Изменение пароля пользователя.
    """

    serializer_class = EmptySerializer

    def post(self, request: Request) -> Response:
        data = request.data
        current_password = data.get('currentPassword')
        new_password = data.get('newPassword')
        user = request.user
        username = user.username
        if user.check_password(current_password):
            user.set_password(new_password)
            user.save()
            user = authenticate(
                request,
                username=username,
                password=new_password,
            )
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


@extend_schema(tags=['Auth'])
class AvatarChangeAPIView(APIView):
    """
    Добавить или обновить аватар пользователя.
    """

    serializer_class = EmptySerializer

    def post(self, request: Request) -> Response:
        avatar = request.FILES['avatar']

        if avatar:
            if Avatar.objects.filter(user_id=request.user.pk).exists():
                user_avatar = Avatar.objects.get(user_id=request.user.pk)
                user_avatar.src = avatar
                user_avatar.save()
                return Response(status=status.HTTP_200_OK)
            else:
                print('Пришел получать профиль')
                profile = Profile.objects.get(user_id=request.user.pk)
                Avatar.objects.create(
                    user_id=profile.pk,
                    src=avatar,
                )
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
