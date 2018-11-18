"""ironman URL Configuration."""
from django.conf.urls import url, include
from ironman.core import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^dashboard/$', views.UserDashboard.as_view(), name='user_dashboard'),
    url(r'^accounts/signup/$', views.UserSignup.as_view(), name='signup'),
]
