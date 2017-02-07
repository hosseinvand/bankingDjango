from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import FormView
from django.views.generic import TemplateView
from django.views.generic import UpdateView

from core.forms.manager import BranchEmployeeCreateForm, ATMCreateForm, SetMaintainerForATMForm
from core.mixin import ManagerRequired
from core.models import Auditor, Employee, ATM, Maintainer
from core.models import Jursit, Cashier
from core.views.admin import EmployeeCreateView


class BranchEmployeeCreateView(ManagerRequired, FormView):
    template_name = 'core/simple_from_with_single_button.html'
    success_url = reverse_lazy('core:main_panel')
    form_class = BranchEmployeeCreateForm

    def form_valid(self, form):
        response = super(BranchEmployeeCreateView, self).form_valid(form)
        form.save()
        return response

    def get_form_kwargs(self):
        kwargs = super(FormView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class BranchEmployeeListView(ManagerRequired, TemplateView):
    template_name = 'core/employee_list.html'

    def get_context_data(self, **kwargs):
        context = super(BranchEmployeeListView, self).get_context_data(**kwargs)
        branch = self.request.user.manager.branch
        context['jursits'] = Jursit.objects.filter(branch=branch)
        context['auditors'] = Auditor.objects.filter(branch=branch)
        context['cashiers'] = Cashier.objects.filter(branch=branch)
        context['maintainers'] = Maintainer.objects.filter(branch=branch)
        return context


class ATMCreateView(ManagerRequired, CreateView):
    model = ATM
    form_class = ATMCreateForm
    template_name = 'core/simple_from_with_single_button.html'
    success_url = reverse_lazy('core:main_panel')

    def get_form_kwargs(self):
        kwargs = super(CreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class SetMaintainerForATMView(ManagerRequired, FormView):
    template_name = 'core/simple_from_with_single_button.html'
    success_url = reverse_lazy('core:main_panel')
    form_class = SetMaintainerForATMForm

    def get_form_kwargs(self):
        kwargs = super(FormView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(SetMaintainerForATMView, self).form_valid(form)
