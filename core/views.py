# -*- coding: utf-8 -*-

import random
import sys
from django.contrib.auth import authenticate, login
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.http.response import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import TemplateView

from core.forms import LoginForm, EmployeeCreateForm, BranchCreateForm, BillTypeCreateForm, \
    Withdraw_Cash_from_Account_form, Add_Cash_to_Account_form, Card_Issuing_form, Transfer_Money_form
from core.models import Customer, Employee, Branch, Account, Manager, Jursit, Auditor, Cashier, BillType, Card
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
    success_url = reverse_lazy('core:cashier_panel')

    def form_valid(self, form):
        response = super(LoginView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response


class EmployeeCreateView(FormView):
    # model = Employee
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


class Withdraw_Cash_from_Account_view(SuccessMessageMixin, CreateView):
    model = Transaction
    template_name = 'core/withdraw_cash_from_account.html'
    success_url = reverse_lazy('core:cashier_panel')
    form_class = Withdraw_Cash_from_Account_form

    # success_message = "%(balance)s" + " برابر است با:  " + "%(last_name)s %(first_name)s  "موجودی جدید حساب
    success_message = "موجودی جدید حساب برابر است با:     %(balance)s"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            first_name = self.object.account.real_owner.first_name,
            last_name = self.object.account.real_owner.last_name,
            balance = self.object.account.balance,
        )

    @transaction.atomic
    def form_valid(self, form):
        temp_form = form.save(commit=False)
        temp_form.cashier = Cashier.objects.get(user__pk =  self.request.user.id)
        temp_form.branch = temp_form.cashier.branch
        temp_form.transaction_type = 'w'
        account = temp_form.account
        account.balance -= temp_form.amount
        account.save()
        temp_form.save()
        return super(Withdraw_Cash_from_Account_view, self).form_valid(form)


class Transfer_Money_view(FormView):
    template_name = 'core/Transfer_Money.html'
    success_url = reverse_lazy('core:cashier_panel')
    form_class = Transfer_Money_form

    @transaction.atomic
    def form_valid(self, form):
        source_account = form.cleaned_data.get('source_account')
        dest_account = form.cleaned_data.get('dest_account')
        amount = form.cleaned_data.get('amount')

        source_account.balance -= amount
        dest_account.balance += amount
        source_account.save()
        dest_account.save()

        trans1 = Transaction(account=source_account, amount=amount, transaction_type='w')
        trans2 = Transaction(account=dest_account, amount=amount, transaction_type='d')
        trans1.cashier = Cashier.objects.get(user__pk =  self.request.user.id)
        trans2.cashier = Cashier.objects.get(user__pk =  self.request.user.id)

        trans1.branch = trans1.cashier.branch
        trans2.branch = trans2.cashier.branch

        trans1.save()
        trans2.save()

        return super(Transfer_Money_view, self).form_valid(form)



class Add_Cash_To_Account_view(CreateView):
    model = Transaction
    template_name = 'core/add_cash_to_account.html'
    success_url = reverse_lazy('core:cashier_panel')
    form_class = Add_Cash_to_Account_form

    @transaction.atomic
    def form_valid(self, form):
        temp_form = form.save(commit=False)
        temp_form.cashier = Cashier.objects.get(user__pk =  self.request.user.id)
        temp_form.branch = temp_form.cashier.branch
        temp_form.transaction_type = 'd'
        account = temp_form.account
        account.balance += temp_form.amount
        account.save()
        temp_form.save()
        return super(Add_Cash_To_Account_view, self).form_valid(form)


class CustomerCreateView(CreateView):
    model = Customer
    template_name = 'core/create_customer.html'
    success_url = reverse_lazy('core:admin_panel')
    form_class = CustomerCreateForm


class Card_Issuing_view(SuccessMessageMixin, CreateView):
    model = Card
    template_name = 'core/card_issue.html'
    success_url = reverse_lazy('core:cashier_panel')
    form_class = Card_Issuing_form
    success_message = "شماره کارت صادر شده: " + " %(card_number)s"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            card_number = self.object.card_number
        )

class AdminPanel(TemplateView):
    template_name = 'core/admin_panel.html'

class CashierPanel(TemplateView):
    template_name = 'core/cashier_panel.html'


class SystemConfigurationView(CreateView):
    form_class = SystemConfigurationForm
    template_name = 'core/sysconfig.html'
    model = SystemConfiguration
    success_url = reverse_lazy('core:admin_panel')

    def __init__(self, *args, **kwargs):
        super(SystemConfigurationView, self).__init__(*args, **kwargs)
        self.config = SystemConfiguration.get_solo()










class TransactionDetailView(generic.DetailView):
    # print("############################################################")
    # print(transactionXX)
    # print("############################################################")
    model = Transaction
    template_name = 'core/transaction_detail.html'

class TransactionsView(generic.ListView):
    model =  Transaction
    template_name = 'core/transactions.html'
    context_object_name = 'transaction_list'

    def get_queryset(self):
        return Transaction.objects.all().order_by('date','time')


# class Account_Transactions_View(FormView):
#     template_name = 'core/account_transaction.html'
#     # success_url = reverse_lazy('core:', kwargs: {'id': account})
#     form_class = Account_Transaction_Form
#
#
#    .r def get_success_url(self):
#         return reverse('offerta create', args=(selfequest.get('account')))
#
#     # @transaction.atomic
#     # def form_valid(self, form):
#     #     account = form.cleaned_data.get('account')
#     #     print("hoooooooooo")
#     #     print(account)
#     #     return super(Account_Transactions_View, self).form_valid(form)
#
#
# class Account_Transactions_selection_View(generic.ListView):
#     model =  Transaction
#     template_name = 'core/transactions.html'
#     context_object_name = 'transaction_list'
#
#     def get_queryset(self):
#         return Transaction.objects.filter(account= input_account).order_by('date','time')












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


class Print_Account_Circulation_view(generic.ListView):
    model = Customer
    template_name = 'core/customers.html'




class CustomerDetailView(generic.DeleteView):
    model = Customer
    template_name = 'core/customer_detail.html'


class BillTypeCreateView(CreateView):
    model = BillType
    form_class = BillTypeCreateForm
    template_name = 'core/bill_type_create.html'
    success_url = reverse_lazy('core:admin_panel')
