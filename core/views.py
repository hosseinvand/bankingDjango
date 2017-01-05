# -*- coding: utf-8 -*-

import random
import sys
from django.contrib.auth import authenticate, login
from django.http.response import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView,CreateView
from core.forms import LoginForm, EmployeeCreateForm, SystemConfigurationForm, BranchCreateForm, CustomerCreateForm
from core.models import Customer, Employee, SystemConfiguration, Branch, Account
from django.shortcuts import render


class LoginView(FormView):
    template_name = 'core/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('mainPage')

    def form_valid(self, form):
        response = super(LoginView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response

class EmployeeCreateView(CreateView):
    model = Employee
    template_name = 'core/create_employee.html'
    success_url = reverse_lazy('mainPage')
    form_class = EmployeeCreateForm

    # def form_valid(self, form):
    #     response = super(SystemUserCreateView, self).form_valid(form)
    #     username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password')
    #     new_user = authenticate(username=username, password=password)
    #     user = User.objects.get(username=username)
    #     SystemUser.objects.filter(user=user).update(role=Patient.load())
    #     login(self.request, new_user)
    #     return response
class BranchCreateView(CreateView):
    model = Branch
    template_name = 'core/create_branch.html'
    success_url = reverse_lazy('mainPage')
    form_class = BranchCreateForm


class AccountCreateView(CreateView):
    model = Customer
    template_name = 'core/create_customer.html'
    success_url = reverse_lazy('mainPage')
    form_class = CustomerCreateForm


class SystemConfigurationView(CreateView):
    form_class = SystemConfigurationForm
    template_name = 'core/sysconfig.html'
    model = SystemConfiguration
    success_url = reverse_lazy('mainPage')
