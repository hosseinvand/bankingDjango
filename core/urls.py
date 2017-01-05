from django.conf.urls import url
from core.views import LoginView, EmployeeCreateView

__author__ = 'mohre'

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^admin/create_employee$', EmployeeCreateView.as_view(), name="create_employee"),
]
