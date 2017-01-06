from django.conf.urls import url
from core.views import LoginView, EmployeeCreateView, BranchCreateView

__author__ = 'mohre'

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^admin/create_employee$', EmployeeCreateView.as_view(), name="create_employee"),
    url(r'^admin/create_branch$', BranchCreateView.as_view(), name="create_branch"),
    # url(r'^cashier/create_account$', AccountCreateView.as_view(), name="create_account"),
]
