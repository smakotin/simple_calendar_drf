from datetime import timedelta
from zoneinfo import ZoneInfo
from django.conf import settings
from calendar_app.models import Event
from calendar_app.tasks import send_notification
from calendar_app.utils import get_calendar_to_city


# def add_country_events_signal(sender, instance, created, **kwargs):
#     if created:
#         if instance.country:
#             country_name = instance.country.country
#             calendar = get_calendar_to_city(country_name)
#             for event in calendar.events:
#                 event = Event.objects.create(
#                     user_id=instance.pk,
#                     title=event.name,
#                     start_time=event.begin.datetime.replace(tzinfo=ZoneInfo(settings.TIME_ZONE)),
#                     end_time=event.end.datetime.replace(tzinfo=ZoneInfo(settings.TIME_ZONE)),
#                     official_holiday=True,
#                 )
#                 event.save()


def send_mail_notification_signal(sender, **kwargs):
    if kwargs['instance'].official_holiday is False:
        start_time = kwargs['instance'].start_time
        user_email = kwargs['instance'].user.email
        notify = kwargs['instance'].notification.notification
        notification_time = start_time - notify

        send_notification.apply_async((user_email,), eta=notification_time)



