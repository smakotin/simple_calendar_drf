from rest_framework.serializers import ModelSerializer

from calendar_app.models import UserEvent, Event


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        exclude = ('user',)


class UserEventSerializer(ModelSerializer):
    event = EventSerializer()

    class Meta:
        model = UserEvent
        fields = ('event',)


class CreateEventSerializer(ModelSerializer):
    class Meta:
        model = Event
        exclude = ('created_at', 'user', 'official_holiday', 'country')



