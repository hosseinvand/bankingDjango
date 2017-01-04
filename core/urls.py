from django.conf.urls import url
from core.views import LoginView

__author__ = 'mohre'

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="login"),
]
