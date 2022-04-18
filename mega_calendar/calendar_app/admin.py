from django.contrib import admin

from calendar_app.models import User, Event, Notification, Country, UserEvent


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'country', 'is_superuser', 'is_active')
    list_editable = ('is_active',)
    list_display_links = ('id', 'username', 'email')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'start_time', 'end_time', 'official_holiday')


@admin.register(UserEvent)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'event_id')
    list_display_links = ('id', 'user_id', 'event_id',)


admin.site.register(Notification)
admin.site.register(Country)
