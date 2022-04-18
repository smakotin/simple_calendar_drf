from calendar_app.models import UserEvent, Event, User
from calendar_app.tasks import send_notification


def add_country_events_signal(sender, instance, **kwargs):
    if instance.country:
        user_holidays = UserEvent.objects.filter(
            user_id=instance.pk,
        )
        if user_holidays.exists():
            user_holidays.delete()
        event_queryset = Event.objects.filter(country_id=instance.country)
        for event in event_queryset:
            user_event = UserEvent.objects.create(
                user_id=instance.pk,
                event_id=event.pk,
            )
            user_event.save()


# def send_mail_notification_signal(sender, **kwargs):
#     if kwargs['instance'].official_holiday is False:
#         start_time = kwargs['instance'].start_time
#         user_email = kwargs['instance'].user.email
#         notify = kwargs['instance'].notification.notification
#         notification_time = start_time - notify
#
#         send_notification.apply_async((user_email,), eta=notification_time)


def add_event_to_user_signal(sender, **kwargs):
    if kwargs['instance'].official_holiday and kwargs['instance'].country_id:
        country_id = kwargs['instance'].country_id
        event_id = kwargs['instance'].id
        user_queryset = User.objects.filter(country_id=country_id)
        for user in user_queryset:
            user_event = UserEvent.objects.create(
                event_id=event_id,
                user_id=user.pk,
            )




