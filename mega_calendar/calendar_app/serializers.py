from rest_framework.serializers import ModelSerializer

from calendar_app.models import Event


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class CreateEventSerializer(ModelSerializer):
    class Meta:
        model = Event
        exclude = ('created_at', 'user', 'official_holiday')



