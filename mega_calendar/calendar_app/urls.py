from django.urls import path, register_converter
from calendar_app.converters import DateConverter
from calendar_app import views
from calendar_app.models import Event
from calendar_app.views import EventFilter

register_converter(DateConverter, 'date')


urlpatterns = [
    path('', views.index, name='index'),
    path('auth/activate/<str:uid>/<str:token>/', views.ActivateUserByEmail.as_view({'get': 'activation'})),
    path('api/events/new/', views.EventsCreateApiView.as_view()),
    path('api/events/', views.EventsListApiView.as_view(), name='events_list'),
    # path('api/events/date/<date:my_date>/', views.EventsDayListApiView.as_view()),
    path('api/events/date/', views.EventsDayListApiView.as_view()),
    path('api/holidays/date/', views.HolidaysListApiView.as_view()),
    path('api/holidays/update/<str:country>', views.UpdateHolidaysToCountry.as_view()),
]
