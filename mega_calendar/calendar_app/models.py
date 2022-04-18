from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint


class User(AbstractUser):
    email = models.EmailField(unique=True)
    country = models.ForeignKey('Country', null=True, blank=True, on_delete=models.SET_NULL)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_country = self.country

    def save(self, *args, **kwargs):
        if self.country and self.old_country != self.country:
            user_holidays = UserEvent.objects.filter(
                user_id=self.pk,
            )
            if user_holidays.exists():
                user_holidays.delete()
            event_queryset = Event.objects.filter(country_id=self.country_id)
            user_event_list = []
            for event in event_queryset:
                user_event = UserEvent(
                    user_id=self.pk,
                    event_id=event.pk,
                )
                user_event_list.append(user_event)
            UserEvent.objects.bulk_create(user_event_list, ignore_conflicts=True)
            self.old_country = self.country
        if not self.country and self.old_country:
            user_holidays = UserEvent.objects.filter(
                user_id=self.pk,
            )
            if user_holidays.exists():
                user_holidays.delete()
            self.old_country = None
        return super().save(*args, **kwargs)


class Country(models.Model):
    country = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.country


class Notification(models.Model):
    notification = models.DurationField(default='01:00:00')  # [DD] [[HH:]MM:]ss[.uuuuuu] format.

    @classmethod
    def get_default_notification(cls):
        obj, created = cls.objects.get_or_create(notification='01:00:00')
        return obj.pk

    def __str__(self):
        return str(self.notification)


class Event(models.Model):
    user = models.ManyToManyField(User, through='UserEvent', blank=True)
    title = models.CharField(max_length=150)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    notification = models.ForeignKey(
        Notification, null=True,
        on_delete=models.SET_NULL,
        default=None
    )
    official_holiday = models.BooleanField(default=False, db_index=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.end_time:
            self.end_time = self.start_time.replace(hour=23, minute=59)
        if self.start_time > self.end_time:
            self.start_time, self.end_time = self.end_time, self.start_time
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        constraints = [
            UniqueConstraint(fields=['title', 'start_time', 'end_time'], name='unique_events')
        ]


class UserEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)




