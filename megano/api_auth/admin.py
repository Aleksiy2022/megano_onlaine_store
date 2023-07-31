from django.contrib import admin
from .models import Profile, Avatar


class ProfileInline(admin.StackedInline):
    model = Avatar


@admin.register(Profile)
class Profile(admin.ModelAdmin):
    list_display = ['id', 'fullName', 'balance', 'user_id', 'phone']

    inlines = [
        ProfileInline
    ]

