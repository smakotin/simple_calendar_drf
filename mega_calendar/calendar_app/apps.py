from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save


class CalendarAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'calendar_app'

    def ready(self):
        from calendar_app import signals
        from calendar_app.models import Event
        User = get_user_model()

        post_save.connect(signals.add_country_events_signal, sender=User)
        post_save.connect(signals.send_mail_notification_signal, sender=Event)
