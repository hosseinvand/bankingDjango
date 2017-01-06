from django.conf.urls import url
from core.views import LoginView,EmployeeCreateView,BranchCreateView,AccountCreateView,SystemConfigurationView, \
    EmployeeListView

from core import views
__author__ = 'mohre'
app_name = 'core'

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^admin/create_employee$', EmployeeCreateView.as_view(), name="create_employee"),
    url(r'^admin/employee_list$', EmployeeListView.as_view(), name="employee_list"),
    url(r'^sysconf/$', SystemConfigurationView.as_view(), name="SystemConfiguration"),
    url(r'^admin/create_branch$', BranchCreateView.as_view(), name="create_branch"),
    url(r'^cashier/create_account$', AccountCreateView.as_view(), name="create_account"),
    url(r'^transactions/$' ,views.TransactionsView.as_view(), name='transactions'),
    url(r'^transactions/(?P<pk>[0-9]+)/$' ,views.TransactionDetailView.as_view(), name='transaction_detail'),
]
