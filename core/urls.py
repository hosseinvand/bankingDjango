from django.conf.urls import url
from core.views import LoginView,EmployeeCreateView,BranchCreateView,AccountCreateView,SystemConfigurationView, \
    EmployeeListView, BranchListView, AdminPanel, BillTypeCreateView, CustomerCreateView

from core import views
app_name = 'core'

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^admin/create_employee$', EmployeeCreateView.as_view(), name="create_employee"),
    url(r'^admin/employee_list$', EmployeeListView.as_view(), name="employee_list"),
    url(r'^admin/branch_list$', BranchListView.as_view(), name="branch_list"),
    url(r'^admin/sysconf/$', SystemConfigurationView.as_view(), name="SystemConfiguration"),
    url(r'^admin/create_branch/$', BranchCreateView.as_view(), name="create_branch"),
    url(r'^admin/create_bill_type/$', BillTypeCreateView.as_view(), name="create_bill_type"),
    url(r'^admin/panel/$', AdminPanel.as_view(), name="admin_panel"),
    url(r'^cashier/create_account/$', AccountCreateView.as_view(), name="create_account"),
    url(r'^cashier/create_customer/$', CustomerCreateView.as_view(), name="create_customer"),
    url(r'^transactions/?$' ,views.TransactionsView.as_view(), name='transactions'),
    url(r'^transactions/(?P<pk>[0-9]+)/$' ,views.TransactionDetailView.as_view(), name='transaction_detail'),
    url(r'^accounts/$' ,views.AccountsView.as_view(), name='accounts'),
    url(r'^accounts/(?P<pk>.{36})/$' ,views.AccountDetailView.as_view(), name='account_detail'),
    url(r'^customers/$' ,views.CustomersView.as_view(), name='customers'),
    url(r'^customers/(?P<pk>[0-9]+)/$' ,views.CustomerDetailView.as_view(), name='customer_detail'),


]
