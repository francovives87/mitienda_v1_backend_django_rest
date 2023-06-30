from django import urls
from django.urls import path, re_path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter


from . import views

app_name = 'realtime_app'




urlpatterns = [
    path(
        'api/v1.0/test',
        views.test.as_view(),
        name='test'
    ),
]