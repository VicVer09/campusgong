from django.urls import path
from . import views

urlpatterns = [
        path('get_schedule', views.get_schedule, name='get_schedule'),
        path('check_valid', views.check_valid, name='check_valid'),
        path('check_update', views.check_update, name='check_update'),
        path('message', views.message, name='message'),
]

