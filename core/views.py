import random

import sys

from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic import FormView

from core.forms import LoginForm
from core.models import Customer
from core.models import Account
from django.shortcuts import render


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('mainPage')

    def form_valid(self, form):
        response = super(LoginView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response
    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['submit_button'] = 'Login'
        return context




def Transfer_cash(request):
    if request.method != 'POST':
        print("kharaab shod2?!!")
    Transfer_amount =  request.POST['Transfer_amount']
    destination_account_number =  request.POST['destination_account_number']
    account = Account.objects.filter(account_number = destination_account_number)[0]
    account.balance += Transfer_amount #TODO in kar (+=) doroste?!
    account.save()


def Account_Opening(request):
    if request.method != 'POST':
        print("kharaab shod1?!!")
    firstName = request.POST['firstName']
    lastName = request.POST['lastName']

    customer = Customer.objects.filter(first_name = firstName, last_name = lastName)[0]
    temp_account_number = random.randint(1, sys.maxsize )
    while len(Account.objects.filter(account_number = temp_account_number)) > 0:
        temp_account_number = random.randint(1, sys.maxsize)

    account = Account(owner = Customer, account_number = temp_account_number, balance = 0)
    account.save()


