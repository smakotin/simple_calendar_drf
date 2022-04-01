from django.urls import path, register_converter

from calendar_app.converters import DateConverter
from calendar_app import views

register_converter(DateConverter, 'date')


urlpatterns = [
    path('', views.index, name='index'),
    path('auth/activate/<str:uid>/<str:token>/', views.ActivateUserByEmail.as_view({'get': 'activation'})),

    path('api/events/new/', views.EventsCreateApiView.as_view()),
    path('api/events/', views.EventsListApiView.as_view()),
    path('api/events/date/<date:my_date>/', views.EventsDayListApiView.as_view()),
]
