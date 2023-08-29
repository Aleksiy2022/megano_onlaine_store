from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    """
    Расширение модели User.
    """

    objects = models.Manager()

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    fullName = models.CharField(max_length=150, null=True)
    phone = PhoneNumberField(unique=True, null=True)
    second_email = models.EmailField(unique=True, null=True)
    balance = models.BigIntegerField(blank=True, null=True)


def user_avatar_directory_path(instance: "Avatar", filename: str) -> str:
    return 'users/user_{pk}/avatar/{filename}'.format(
        pk=instance.user_id,
        filename=filename,
    )


class Avatar(models.Model):
    """
    Модель для хранения Аватара пользователя.
    """

    objects = models.Manager()

    user = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name='avatar'
    )
    src = models.ImageField(upload_to=user_avatar_directory_path)
    alt = models.CharField(max_length=200)
