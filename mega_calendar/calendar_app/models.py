from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=100, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'country']


class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    event_date = models.DateField()  # format 'YYYY-MM-DD'
    start_time = models.TimeField(default='00:00')
    end_time = models.TimeField(default='23:59')
    created_at = models.DateTimeField(auto_now_add=True)
    notification = models.ForeignKey('Notification', on_delete=models.CASCADE)


class Notification(models.Model):
    notification = models.DurationField(default='01:00:00')  # [DD] [[HH:]MM:]ss[.uuuuuu] format.

    def __str__(self):
        return self.notification
