from django.urls import path
from calendar_app.views import index, ActivateUserByEmail

urlpatterns = [
    path('', index, name='index'),
    path('auth/activate/<str:uid>/<str:token>/', ActivateUserByEmail.as_view({'get': 'activation'})),
]
