from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from calendar_app.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'city')
