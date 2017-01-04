import random

import sys

from django.contrib.auth import authenticate, login
from django.http.response import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView

from core.forms import LoginForm
from core.models import Customer
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

    # def get_context_data(self, **kwargs):
    #     context = super(LoginView, self).get_context_data(**kwargs)
    #     context['submit_button'] = 'Login'
    #     return context

