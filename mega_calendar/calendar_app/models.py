from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    country = models.ForeignKey('Country', null=True, blank=True, on_delete=models.CASCADE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    notification = models.ForeignKey('Notification', on_delete=models.CASCADE)
    official_holiday = models.BooleanField(default=False)


class Country(models.Model):
    country = models.CharField(max_length=100, unique=True)


class Notification(models.Model):
    notification = models.DurationField(default='01:00:00')  # [DD] [[HH:]MM:]ss[.uuuuuu] format.

    def __str__(self):
        return self.notification
