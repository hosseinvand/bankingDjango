from django.conf.urls import url
<<<<<<< HEAD
from core.views import LoginView, EmployeeCreateView,SystemConfigurationView
=======
from core.views import LoginView, EmployeeCreateView, BranchCreateView, AccountCreateView
>>>>>>> 981428c1f79ac3c3241765d8b40aa22dea86eb4b

__author__ = 'mohre'

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^admin/create_employee$', EmployeeCreateView.as_view(), name="create_employee"),
<<<<<<< HEAD
    url(r'^sysconf/$', SystemConfigurationView.as_view(), name="SystemConfiguration"),
=======
    url(r'^admin/create_branch$', BranchCreateView.as_view(), name="create_branch"),
    url(r'^cashier/create_account$', AccountCreateView.as_view(), name="create_account"),
>>>>>>> 981428c1f79ac3c3241765d8b40aa22dea86eb4b
]
