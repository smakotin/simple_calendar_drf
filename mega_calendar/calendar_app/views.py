# from datetime import timedelta
# from django.db.models import Q
from zoneinfo import ZoneInfo

from django.conf import settings
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from tatsu.exceptions import FailedParse
from tqdm import tqdm

from calendar_app.models import Event, Country
from calendar_app.serializers import CreateEventSerializer, EventSerializer

from django_filters import rest_framework as filters

from calendar_app.utils import get_calendar_to_city


def index(request):
    return render(request, 'calendar_app/index.html', context={'user': request.user})


class EventFilter(filters.FilterSet):
    from_date = filters.DateTimeFilter(field_name="start_time", lookup_expr='gte')
    to_date = filters.DateTimeFilter(field_name="end_time", lookup_expr='lte')


class ActivateUserByEmail(UserViewSet):
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())

        # this line is the only change from the base implementation.
        kwargs['data'] = {"uid": self.kwargs['uid'], "token": self.kwargs['token']}

        return serializer_class(*args, **kwargs)

    def activation(self, request, uid, token, *args, **kwargs):
        super().activation(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)


class EventsCreateApiView(CreateAPIView):
    serializer_class = CreateEventSerializer
    queryset = Event.objects

    def perform_create(self, serializer):
        serializer.save(user=(self.request.user.pk,))


class EventsListApiView(ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Event.objects.prefetch_related('user').filter(
            user=user
        )
        return queryset


class EventsDayListApiView(ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EventFilter

    def get_queryset(self):
        queryset = Event.objects.filter(user=self.request.user)
        return queryset


class HolidaysListApiView(ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EventFilter

    def get_queryset(self):
        queryset = Event.objects.filter(
            user=self.request.user,
            official_holiday=True
        )
        return queryset

    # def get_queryset(self):
    #     user = self.request.user
    #     my_date = self.kwargs['my_date']
    #     end_my_date = my_date + timedelta(hours=24)
    #     queryset = Event.objects.filter(
    #         Q(user_id=user.pk)
    #         & (
    #             Q(start_time__gte=my_date, end_time__lt=end_my_date)
    #             | Q(start_time__lte=my_date, end_time__gte=my_date, end_time__lt=end_my_date)
    #             | Q(start_time__gte=my_date, start_time__lt=end_my_date, end_time__gt=end_my_date)
    #             | Q(start_time__lte=my_date, end_time__gt=end_my_date)
    #         )
    #     )
    #     return queryset


class UpdateHolidaysToCountry(APIView):
    def get(self, request, *args, **kwargs):
        country = kwargs['country'].capitalize()
        country_id = Country.objects.get(country=country).pk
        event_obj_lst = []
        try:
            calendar = get_calendar_to_city(country)
            for event in tqdm(calendar.events):
                event_obj = Event(
                    title=event.name,
                    start_time=event.begin.datetime.replace(tzinfo=ZoneInfo(settings.TIME_ZONE)),
                    end_time=event.end.datetime.replace(tzinfo=ZoneInfo(settings.TIME_ZONE)),
                    official_holiday=True,
                    country_id=country_id
                )
                if event_obj not in event_obj_lst:
                    event_obj_lst.append(event_obj)
            try:
                Event.objects.bulk_create(event_obj_lst, ignore_conflicts=True)
            except IntegrityError:
                print(f'.......Error when saving the event {event.name}, maybe duplicate')
            print('complete')
            return Response(status=status.HTTP_200_OK)
        except FailedParse:
            print('FailedParse')
        return Response(status=status.HTTP_417_EXPECTATION_FAILED)




