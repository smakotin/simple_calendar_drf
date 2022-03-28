from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from calendar_app.models import User, Event, Notification


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'city', 'is_superuser', 'is_active')
    list_editable = ('is_active',)
    list_display_links = ('id', 'username', 'email')


admin.site.register(Event)
admin.site.register(Notification)
