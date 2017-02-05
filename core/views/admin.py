# -*- coding: utf-8 -*-

from django.contrib.auth import authenticate, login
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import DeleteView
from django.views.generic import FormView, CreateView
from django.views.generic import ListView
from django.views.generic import TemplateView

from core.forms.admin import BillTypeCreateForm
from core.forms.admin import CustomerCreateForm
from core.forms.admin import LoginForm, EmployeeCreateForm, SystemConfigurationForm, BranchCreateForm, \
    AccountCreateForm
from core.mixin import SuperUserRequired, ManagerOrSuperUserRequired
from core.models import BillType, Card, Employee, Bill, Maintainer
from core.models import Customer, SystemConfiguration, Branch, Account, Transaction
from core.models import Manager, Jursit, Auditor, Cashier


class LoginView(FormView):
    template_name = 'core/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('core:cashier_panel')

    def form_valid(self, form):
        response = super(LoginView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response


class EmployeeCreateView(SuperUserRequired, FormView):
    # model = Employee
    template_name = 'core/simple_from_with_single_button.html'
    success_url = reverse_lazy('core:admin_panel')
    form_class = EmployeeCreateForm

    def form_valid(self, form):
        response = super(EmployeeCreateView, self).form_valid(form)
        form.save()
        return response

    def get_form_kwargs(self):
        kwargs = super(FormView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class EmployeeDeleteView(ManagerOrSuperUserRequired, DeleteView):
    model = Employee
    success_url = reverse_lazy('core:admin_panel')

    def get_queryset(self):
        print(self.request.GET['type'])
        if self.request.GET['type'] == 'manager':
            return Manager.objects.all()
        if self.request.GET['type'] == 'jursit':
            return Jursit.objects.all()
        if self.request.GET['type'] == 'cashier':
            return Cashier.objects.all()
        if self.request.GET['type'] == 'auditor':
            return Auditor.objects.all()



class EmployeeListView(SuperUserRequired, TemplateView):
    template_name = 'core/employee_list.html'

    def get_context_data(self, **kwargs):
        context = super(EmployeeListView, self).get_context_data(**kwargs)
        context['managers'] = Manager.objects.all()
        context['jursits'] = Jursit.objects.all()
        context['auditors'] = Auditor.objects.all()
        context['cashiers'] = Cashier.objects.all()
        context['maintainers'] = Maintainer.objects.all()
        return context


class BranchListView(SuperUserRequired, ListView):
    model = Branch
    template_name = 'core/branch_list.html'

    def get_queryset(self):
        return Branch.objects.all()


class BranchCreateView(SuperUserRequired, CreateView):
    model = Branch
    template_name = 'core/simple_from_with_single_button.html'
    success_url = reverse_lazy('core:admin_panel')
    form_class = BranchCreateForm


class AccountCreateView(SuperUserRequired, CreateView):
    model = Account
    template_name = 'core/simple_from_with_single_button.html'
    success_url = reverse_lazy('core:admin_panel')
    form_class = AccountCreateForm


class CustomerCreateView(SuperUserRequired, CreateView):
    model = Customer
    template_name = 'core/simple_from_with_single_button.html'
    success_url = reverse_lazy('core:admin_panel')
    form_class = CustomerCreateForm



class AdminPanel(SuperUserRequired, TemplateView):
    template_name = 'core/admin_panel.html'


class SystemConfigurationView(SuperUserRequired, CreateView):
    form_class = SystemConfigurationForm
    template_name = 'core/sysconfig.html'
    model = SystemConfiguration
    success_url = reverse_lazy('core:admin_panel')

    def __init__(self, *args, **kwargs):
        super(SystemConfigurationView, self).__init__(*args, **kwargs)
        self.config = SystemConfiguration.get_solo()

class TransactionDetailView(generic.DetailView):
    model = Transaction
    template_name = 'core/transaction_detail.html'


class TransactionsView(generic.ListView):
    model = Transaction
    template_name = 'core/transactions.html'
    context_object_name = 'transaction_list'
    def get_queryset(self):
        return Transaction.objects.all().order_by('date', 'time')


class AccountsView(SuperUserRequired, ListView):
    model = Account
    template_name = 'core/accounts.html'

    def get_queryset(self):
        return Account.objects.all()


class AccountDetailView(SuperUserRequired, generic.DetailView):
    model = Account
    template_name = 'core/account_detail.html'


class CustomersView(SuperUserRequired, generic.ListView):
    model = Customer
    template_name = 'core/customers.html'

    def get_queryset(self):
        return Customer.objects.all()


class Print_Account_Circulation_view(generic.ListView):
    model = Customer
    template_name = 'core/customers.html'


class CustomerDetailView(SuperUserRequired, generic.DeleteView):
    model = Customer
    template_name = 'core/customer_detail.html'


class BillTypeCreateView(SuperUserRequired, CreateView):
    model = BillType
    form_class = BillTypeCreateForm
    template_name = 'core/simple_from_with_single_button.html'
    success_url = reverse_lazy('core:admin_panel')


