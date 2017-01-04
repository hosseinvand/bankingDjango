from django.conf.urls import url
from django.contrib.auth.views import logout

from reservation import views
from reservation.views import *

__author__ = 'mohre'

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="login"),
]
