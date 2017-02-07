from django.db import transaction
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic.edit import UpdateView

from core.forms.jursit import Block_Account_form, Jursit_ChequeDetail_Form, Jursit_LoanDetail_Form
from core.models import ChequeIssue, Account, Cashier, Transaction, LoanApplication


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



class Jursit_Check_Issue_Requests_view(ListView):
    model = ChequeIssue
    template_name = 'core/jursit_cheque_issue.html'
    context_object_name = 'cheque_issue_list'

    def get_queryset(self):
        return ChequeIssue.objects.filter(legal_expert_validation= 'NA').order_by('date')



class Jursit_ChequeDetailView(UpdateView):
    model = ChequeIssue
    template_name = 'core/jursit_cheque_detail.html'
    success_url = reverse_lazy('core:main_panel')
    form_class = Jursit_ChequeDetail_Form

    def form_valid(self, form):
        legal_expert_validation = form.cleaned_data.get('legal_expert_validation')
        cheque_issue = ChequeIssue.objects.get(id=self.kwargs['pk'])
        cheque_issue.legal_expert_validation = legal_expert_validation
        cheque_issue.save()
        return super(Jursit_ChequeDetailView, self).form_valid(form)


class Jursit_Loan_Requests_view(ListView):
    model = LoanApplication
    template_name = 'core/jursit_loan_issue.html'
    context_object_name = 'loan_list'

    def get_queryset(self):
        return LoanApplication.objects.filter(legal_expert_validation= 'NA')



class Jursit_LoanDetailView(UpdateView):
    model = LoanApplication
    template_name = 'core/jursit_loan_detail.html'
    success_url = reverse_lazy('core:main_panel')
    form_class = Jursit_LoanDetail_Form

    def form_valid(self, form):
        legal_expert_validation = form.cleaned_data.get('legal_expert_validation')
        loan_application = LoanApplication.objects.get(id=self.kwargs['pk'])
        loan_application.legal_expert_validation = legal_expert_validation
        loan_application.save()
        return super(Jursit_LoanDetailView, self).form_valid(form)


