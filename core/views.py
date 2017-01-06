# -*- coding: utf-8 -*-

import random
import sys
from django.contrib.auth import authenticate, login
from django.http.response import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import TemplateView

from core.forms import LoginForm, EmployeeCreateForm, BranchCreateForm, BillTypeCreateForm
from core.models import Customer, Employee, Branch, Account, Manager, Jursit, Auditor, Cashier, BillType
from core.forms import LoginForm, EmployeeCreateForm, BranchCreateForm, CustomerCreateForm
from core.models import Customer, Employee, Branch, Account, Manager, Jursit, Auditor, Cashier
from django.views.generic import FormView, UpdateView,CreateView
from core.forms import LoginForm, EmployeeCreateForm, SystemConfigurationForm, BranchCreateForm, \
    AccountCreateForm
from core.models import Customer, Employee, SystemConfiguration, Branch, Account,Transaction
from django.shortcuts import render
from django.views import generic


class LoginView(FormView):
    template_name = 'core/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('core:admin_panel')

    def form_valid(self, form):
        response = super(LoginView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response


class EmployeeCreateView(FormView):
    model = Employee
    template_name = 'core/create_employee.html'
    success_url = reverse_lazy('core:admin_panel')
    form_class = EmployeeCreateForm

    def form_valid(self, form):
        response = super(EmployeeCreateView, self).form_valid(form)
        form.save()
        return response


class EmployeeListView(TemplateView):
    template_name = 'core/employee_list.html'

    def get_context_data(self, **kwargs):
        context = super(EmployeeListView, self).get_context_data(**kwargs)
        context['managers'] = Manager.objects.all()
        context['jursits'] = Jursit.objects.all()
        context['auditors'] = Auditor.objects.all()
        context['cashiers'] = Cashier.objects.all()
        return context


class BranchListView(ListView):
    model = Branch
    template_name = 'core/branch_list.html'

    def get_queryset(self):
        return Branch.objects.all()


class BranchCreateView(CreateView):
    model = Branch
    template_name = 'core/create_branch.html'
    success_url = reverse_lazy('core:admin_panel')
    form_class = BranchCreateForm


class AccountCreateView(CreateView):
    model = Account
    template_name = 'core/create_account.html'
    success_url = reverse_lazy('core:admin_panel')
    form_class = AccountCreateForm

class CustomerCreateView(CreateView):
    model = Customer
    template_name = 'core/create_customer.html'
    success_url = reverse_lazy('core:admin_panel')
    form_class = CustomerCreateForm


class AdminPanel(TemplateView):
    template_name = 'core/admin_panel.html'


class SystemConfigurationView(CreateView):
    config = SystemConfiguration.get_solo()
    form_class = SystemConfigurationForm
    template_name = 'core/sysconfig.html'
    model = SystemConfiguration
    success_url = reverse_lazy('core:admin_panel')


class TransactionsView(generic.ListView):
    model =  Transaction
    template_name = 'core/transactions.html'
    context_object_name = 'transaction_list'

    def get_queryset(self):
        return Transaction.objects.all().order_by('date','time')


class TransactionDetailView(generic.DetailView):
    model = Transaction
    template_name = 'core/transaction_detail.html'


class AccountsView(ListView):
    model = Account
    template_name = 'core/accounts.html'

    def get_queryset(self):
        return Account.objects.all()


class AccountDetailView(generic.DetailView):
    model = Account
    template_name = 'core/account_detail.html'


class CustomersView(generic.ListView):
    model = Customer
    template_name = 'core/customers.html'

    def get_queryset(self):
        return Customer.objects.all()


class CustomerDetailView(generic.DeleteView):
    model = Customer
    template_name = 'core/customer_detail.html'


class BillTypeCreateView(CreateView):
    model = BillType
    form_class = BillTypeCreateForm
    template_name = 'core/bill_type_create.html'
    success_url = reverse_lazy('core:admin_panel')
