from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from users import models

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'username',
        'id',
        'email',
        'first_name',
        'last_name',
    )
    list_filter = ('email', 'first_name')


@admin.register(models.Subscribes)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)
