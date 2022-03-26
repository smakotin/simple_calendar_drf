from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=100, blank=True)

    REQUIRED_FIELDS = ['email', 'city']


