from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from cart.utils import merge_carts
from .models import Profile, Avatar


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]


class UserRegisterSerializer(serializers.ModelSerializer):

    name = serializers.CharField()

    class Meta:
        model = User
        fields = [
            'name',
            'username',
            'password',
        ]

    def save(self, request):
        # Создаём объект класса User
        name = self.validated_data['name']
        username = self.validated_data['username']
        password = self.validated_data['password']
        new_user = User(
            first_name=name,
            username=username,
        )
        new_user.set_password(password)
        new_user.save()
        Profile.objects.create(user=new_user)
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        merge_carts(request=request, user=user)
        login(request, user=user)
        return new_user


class AvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Avatar
        fields = (
            'src',
            'alt',
        )


class ProfileSerializer(serializers.ModelSerializer):

    avatar = AvatarSerializer()
    email = serializers.EmailField(source='second_email')

    class Meta:
        model = Profile
        fields = [
            'fullName',
            'email',
            'phone',
            'avatar',
        ]


class ChangePasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'currentPassword',
            'newPassword',
        ]


class ChangeAvatarSerializer(serializers.ModelSerializer):

    avatar = serializers.ImageField(source='src')

    class Meta:
        model = Avatar
        fields = [
            'avatar',
        ]

class EmptySerializer(serializers.Serializer):
    pass