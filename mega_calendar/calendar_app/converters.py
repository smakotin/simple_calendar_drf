from datetime import datetime, timezone


class DateConverter:
    regex = '\d{4}-\d{1,2}-\d{1,2}'
    format = '%Y-%m-%d'

    def to_python(self, value):
        return datetime.strptime(value, self.format).replace(tzinfo=timezone.utc)

    def to_url(self, value):
        return value.strftime(self.format)
