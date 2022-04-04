from datetime import datetime
from zoneinfo import ZoneInfo

from django.conf import settings


class DateConverter:
    regex = '\d{4}-\d{1,2}-\d{1,2}'
    format = '%Y-%m-%d'

    def to_python(self, value):
        return datetime.strptime(value, self.format).replace(tzinfo=ZoneInfo(settings.TIME_ZONE)) # TODO django filters

    def to_url(self, value):
        return value.strftime(self.format)
