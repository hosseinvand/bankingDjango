from django.db import transaction
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView
from django.views.generic import FormView
from django.views.generic import ListView

from core.forms.jursit import Block_Account_form
from core.models import ChequeIssue


class Block_Account_view(FormView):
    template_name = 'core/simple_from_with_single_button.html'
    success_url = reverse_lazy('core:main_panel')
    form_class = Block_Account_form

    @transaction.atomic
    def form_valid(self, form):
        account = form.cleaned_data.get('account')
        account.is_blocked = True
        account.save()
        return super(Block_Account_view, self).form_valid(form)

#
# class Block_Account_view(FormView):
#     template_name = 'core/simple_from_with_single_button.html'
#     success_url = reverse_lazy('core:main_panel')
#     form_class = Block_Account_form
#
#     @transaction.atomic
#     def form_valid(self, form):
#         account = form.cleaned_data.get('account')
#         account.is_blocked = True
#         account.save()
#
#         return super(Block_Account_view, self).form_valid(form)
#



class Check_Issue_Requests_view(ListView):
    model = ChequeIssue
    template_name = 'core/cheque_issue.html'
    context_object_name = 'cheque_issue_list'

    def get_queryset(self):
        return ChequeIssue.objects.filter(legal_expert_validation= 'NA').order_by('date')



class ChequeDetailView(generic.DetailView):
    model = ChequeIssue
    template_name = 'core/cheque_detail.html'
