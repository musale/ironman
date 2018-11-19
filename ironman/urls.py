"""ironman URL Configuration."""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from ironman.core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.ActivateAccountView.as_view(), name='activate_account'),
    url(r'', include('ironman.core.urls')),

]
