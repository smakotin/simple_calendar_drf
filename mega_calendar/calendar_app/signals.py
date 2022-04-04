from zoneinfo import ZoneInfo
from django.conf import settings
from calendar_app.models import Event
from calendar_app.utils import get_calendar_to_city


def add_country_events_signal(sender, instance, created, **kwargs):
    if created:
        if instance.country:
            country_name = instance.country.country
            calendar = get_calendar_to_city(country_name)
            for event in calendar.events:
                event = Event.objects.create(
                    user_id=instance.pk,
                    title=event.name,
                    start_time=event.begin.datetime.replace(tzinfo=ZoneInfo(settings.TIME_ZONE)),
                    end_time=event.end.datetime.replace(tzinfo=ZoneInfo(settings.TIME_ZONE)),
                    official_holiday=True,
                )
                event.save()



