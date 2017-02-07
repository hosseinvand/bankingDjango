from django.conf.urls import url
from django.urls import reverse_lazy

from core.views.admin import LoginView, EmployeeCreateView, BranchCreateView, AccountCreateView, \
    SystemConfigurationView, \
    EmployeeListView, BranchListView, AdminPanel, BillTypeCreateView, CustomerCreateView, \
    AccountDetailView, TransactionDetailView, TransactionsView, AccountsView, CustomersView, CustomerDetailView, EmployeeDeleteView, \
    MainPanel, GreenbackCreateView
from django.contrib.auth.views import logout
from django.urls import reverse_lazy

from core.views.atm import LoginATM, PanelATM, WithdrawATM
from core.views.jursit import Block_Account_view, Check_Issue_Requests_view, ChequeDetailView
from core.views.admin import LoginView, EmployeeCreateView, BranchCreateView, SystemConfigurationView, \
    EmployeeListView, BranchListView, AdminPanel, BillTypeCreateView, AccountDetailView, TransactionDetailView, TransactionsView, AccountsView, CustomersView, CustomerDetailView, EmployeeDeleteView, \
    GreenbackCreateView
# from core.views.cashier import Bill_Create_view
from core.views.maintainer import SetGreenbackForATMView
from core.views.manager import BranchEmployeeListView, BranchEmployeeCreateView, ATMCreateView, \
    SetMaintainerForATMView

EmployeeListView, BranchListView, AdminPanel, BillTypeCreateView, CustomerCreateView, \
    AccountDetailView, TransactionDetailView, TransactionsView, AccountsView, CustomersView, CustomerDetailView
from core.views.cashier import Bill_Payment_view, Account_Transactions_View, Account_Transactions_Selection_View, \
    Bill_Create_view, CashierPanel, Add_Cash_To_Account_view, Withdraw_Cash_from_Account_view, Transfer_Money_view, \
    Card_Issuing_view, Cheque_Application_view, Cheque_Issue_Cash_view, Cheque_Issue_toAccount_view, Loan_Request_view, \
    Payment_Order_view

app_name = 'core'

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', logout, {'next_page': reverse_lazy('core:login')}, name='logout'),
    url(r'^admin/create_greenback/$', GreenbackCreateView.as_view(), name="create_greenback"),
    url(r'^admin/create_employee/$', EmployeeCreateView.as_view(), name="create_employee"),
    url(r'^admin/employee_list/$', EmployeeListView.as_view(), name="employee_list"),
    url(r'^admin/delete_employee/(?P<pk>[0-9]+)/$', EmployeeDeleteView.as_view(), name="delete_employee"),
    url(r'^admin/branch_list/$', BranchListView.as_view(), name="branch_list"),
    url(r'^admin/sysconf/$', SystemConfigurationView.as_view(), name="SystemConfiguration"),
    url(r'^admin/create_branch/$', BranchCreateView.as_view(), name="create_branch"),
    url(r'^admin/create_bill_type/$', BillTypeCreateView.as_view(), name="create_bill_type"),
    url(r'^admin/bill_create/$', Bill_Create_view.as_view(), name="bill_create"),
    url(r'^admin/panel/$', AdminPanel.as_view(), name="admin_panel"),
    url(r'^main/panel/$', MainPanel.as_view(), name="main_panel"),
    url(r'^cashier/panel/$', CashierPanel.as_view(), name="cashier_panel"),
    url(r'^cashier/create_account/$', AccountCreateView.as_view(), name="create_account"),
    url(r'^cashier/add_cash/$', Add_Cash_To_Account_view.as_view(), name="add_cash_to_account"),
    url(r'^cashier/withdraw_cash/$', Withdraw_Cash_from_Account_view.as_view(), name="withdraw_cash_from_account"),
    url(r'^cashier/transfer_money/$', Transfer_Money_view.as_view(), name="transfer_money"),
    url(r'^cashier/create_customer/$', CustomerCreateView.as_view(), name="create_customer"),
    url(r'^cashier/bill_payment/$', Bill_Payment_view.as_view(), name="bill_payment"),
    url(r'^cashier/card_issue/$', Card_Issuing_view.as_view(), name="card_issue"),
    url(r'^cashier/cheque_application/$', Cheque_Application_view.as_view(), name="cheque_application"),
    url(r'^cashier/cheque_issue_cash/$', Cheque_Issue_Cash_view.as_view(), name="cheque_issue_cash"),
    url(r'^cashier/cheque_issue_toAccount/$', Cheque_Issue_toAccount_view.as_view(), name="cheque_issue_toAccount"),
    url(r'^cashier/account_transactions/$', Account_Transactions_View.as_view(), name='account_transactions'),
    url(r'^cashier/account_transactions/select/(?P<pk>.+)$', Account_Transactions_Selection_View.as_view(), name='account_transactions_select_view'),
    url(r'^cashier/loan_request/$', Loan_Request_view.as_view(), name="loan_request"),
    url(r'^cashier/payment_order/$', Payment_Order_view.as_view(), name="payment_order"),
    url(r'^transactions/?$', TransactionsView.as_view(), name='transactions'),
    url(r'^transactions/(?P<pk>[0-9]+)/$', TransactionDetailView.as_view(), name='transaction_detail'),
    url(r'^accounts/$', AccountsView.as_view(), name='accounts'),
    url(r'^accounts/(?P<pk>.{36})/$', AccountDetailView.as_view(), name='account_detail'),
    url(r'^customers/$', CustomersView.as_view(), name='customers'),
    url(r'^customers/(?P<pk>[0-9]+)/$', CustomerDetailView.as_view(), name='customer_detail'),
    url(r'^manager/employee_list/$', BranchEmployeeListView.as_view(), name="employee_list_manager"),
    url(r'^manager/create_employee/$', BranchEmployeeCreateView.as_view(), name="create_employee_manager"),
    url(r'^manager/create_atm/$', ATMCreateView.as_view(), name="create_atm"),
    url(r'^manager/set_maintainer/$', SetMaintainerForATMView.as_view(), name="set_maintainer"),
    url(r'^maintainer/set_greenback/$', SetGreenbackForATMView.as_view(), name="set_greenback"),
    url(r'^jursit/block_account/$', Block_Account_view.as_view(), name="block_account"),
    url(r'^jursit/check_issue_requests/$', Check_Issue_Requests_view.as_view(), name="cheque_issue_requests"),
    url(r'^jursit/check_issue_requests/(?P<pk>[0-9]+)/$', ChequeDetailView.as_view(), name='cheque_detail'),
    url(r'^atm/login/$', LoginATM.as_view(), name='atm_login'),
    url(r'^atm/panel/(?P<atm>[0-9]+)/(?P<card_number>.+)/$', PanelATM.as_view(), name='atm_panel'),
    url(r'^atm/withdraw/(?P<atm>[0-9]+)/(?P<card_number>.+)/$', WithdrawATM.as_view(), name='atm_withdraw'),
]
