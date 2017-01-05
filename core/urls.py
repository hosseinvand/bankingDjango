from django.conf.urls import url
from core.views import LoginView, MakeBranch

__author__ = 'mohre'

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^makebranch/$', MakeBranch.as_view(), name="MakeBranch"),
]
