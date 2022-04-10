from rest_framework.serializers import ModelSerializer

from calendar_app.models import UserEvent, Event


class UserEventSerializer(ModelSerializer):
    class Meta:
        model = UserEvent
        fields = '__all__'
        depth = 1


class CreateEventSerializer(ModelSerializer):
    class Meta:
        model = Event
        exclude = ('created_at', 'user', 'official_holiday', 'country')



