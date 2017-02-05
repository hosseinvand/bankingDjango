from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic import TemplateView

from core.forms.manager import BranchEmployeeCreateForm
from core.mixin import ManagerRequired
from core.models import Auditor
from core.models import Jursit, Cashier
from core.views.admin import EmployeeCreateView


class BranchEmployeeCreateView(ManagerRequired, FormView):
    template_name = 'core/simple_from_with_single_button.html'
    success_url = reverse_lazy('core:manager_panel')
    form_class = BranchEmployeeCreateForm

    def form_valid(self, form):
        response = super(BranchEmployeeCreateView, self).form_valid(form)
        form.save()
        return response

    def get_form_kwargs(self):
        kwargs = super(FormView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class BranchEmployeeListView(TemplateView):
    template_name = 'core/employee_list.html'

    def get_context_data(self, **kwargs):
        context = super(BranchEmployeeListView, self).get_context_data(**kwargs)
        branch = self.request.user.manager.branch
        context['jursits'] = Jursit.objects.filter(branch=branch)
        context['auditors'] = Auditor.objects.filter(branch=branch)
        context['cashiers'] = Cashier.objects.filter(branch=branch)
        return context
