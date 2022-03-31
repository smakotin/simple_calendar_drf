from django.contrib import admin

from calendar_app.models import User, Event, Notification, Country


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'country', 'is_superuser', 'is_active')
    list_editable = ('is_active',)
    list_display_links = ('id', 'username', 'email')


admin.site.register(Event)
admin.site.register(Notification)
admin.site.register(Country)
