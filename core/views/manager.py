from django.urls import reverse_lazy
from django.views.generic import TemplateView

from core.forms.manager import BranchEmployeeCreateForm
from core.models import Auditor
from core.models import Jursit, Cashier
from core.views.admin import EmployeeCreateView


class BranchEmployeeCreateView(EmployeeCreateView):
    success_url = reverse_lazy('core:manager_panel')
    form_class = BranchEmployeeCreateForm

# class BranchEmployeeListView(TemplateView):
#     template_name = 'core/employee_list.html'
#
#     def get_context_data(self, **kwargs):
#         #branch = self.user.branch # TODO
#         context = super(BranchEmployeeListView, self).get_context_data(**kwargs)
#         context['jursits'] = Jursit.objects.filter(branch=)
#         context['auditors'] = Auditor.objects.all()
#         context['cashiers'] = Cashier.objects.all()
#         return context
