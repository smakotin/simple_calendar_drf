# from datetime import timedelta
# from django.db.models import Q
from django.shortcuts import render
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from calendar_app.models import Event, UserEvent
from calendar_app.serializers import CreateEventSerializer, UserEventSerializer, EventSerializer

from django_filters import rest_framework as filters


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
        serializer.save(user=(self.request.user.pk,)) ## TODO


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
