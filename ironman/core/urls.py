"""ironman URL Configuration."""
from django.conf.urls import url
from ironman.core import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index')
]
