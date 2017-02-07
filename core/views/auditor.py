from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic import UpdateView

from core.forms.auditor import Auditor_ChequeDetail_Form, Auditor_LoanDetail_Form
from core.models import Cashier, Transaction, ChequeIssue, LoanApplication


class Auditor_Check_Issue_Requests_view(ListView):
    model = ChequeIssue
    template_name = 'core/auditor_cheque_issue.html'
    context_object_name = 'cheque_issue_list'

    def get_queryset(self):
        return ChequeIssue.objects.filter(legal_expert_validation= 'AC', auditor_validation='NA').order_by('date')



class Auditor_ChequeDetailView(UpdateView):
    model = ChequeIssue
    template_name = 'core/auditor_cheque_detail.html'
    success_url = reverse_lazy('core:main_panel')
    form_class = Auditor_ChequeDetail_Form
    # fields = ['legal_expert_validation']
    # labels = {
    #     'legal_expert_validation': "نظر کارشناس حقوقی",
    # }

    # def get_object(self, queryset=None):
    # def save(self):
    # def dispatch(self, *args, **kwargs):
    def form_valid(self, form):
        auditor_validation = form.cleaned_data.get('auditor_validation')
        # print(auditor_validation)
        cheque_issue = ChequeIssue.objects.get(id=self.kwargs['pk'])
        cheque_issue.auditor_validation = auditor_validation
        cheque_issue.save()
        # print("HOOOOOOOOOOOOOOOOOOOOOOOOOOO")
        # print(cheque_issue.cheque.cheque_application.account.real_owner.father_name)
        # print(cheque_issue.auditor_validation)
        source_account = cheque_issue.cheque.cheque_application.account
        amount = cheque_issue.amount
        # print(amount)
        source_account.balance -= amount
        source_account.save()

        trans1 = Transaction(account=source_account, amount=amount, transaction_type='w')
        # trans1.cashier = Cashier.objects.get(user__pk=self.request.user.id)
        trans1.cashier = cheque_issue.cashier
        trans1.branch = trans1.cashier.branch
        trans1.save()

        if cheque_issue.dest != None:
            dest_account = cheque_issue.dest
            source_account.balance += amount
            source_account.save()

            trans2 = Transaction(account=dest_account, amount=amount, transaction_type='d')
            trans2.cashier = cheque_issue.cashier
            trans2.branch = trans2.cashier.branch
            trans2.save()


        return super(Auditor_ChequeDetailView, self).form_valid(form)




class Auditor_Loan_Requests_view(ListView):
    model = LoanApplication
    template_name = 'core/auditor_loan_issue.html'
    context_object_name = 'loan_list'

    def get_queryset(self):
        return LoanApplication.objects.filter(legal_expert_validation= 'AC', auditor_validation='NA')



class Auditor_LoanDetailView(UpdateView):
    model = LoanApplication
    template_name = 'core/auditor_loan_detail.html'
    success_url = reverse_lazy('core:main_panel')
    form_class = Auditor_LoanDetail_Form

    def form_valid(self, form):
        auditor_validation = form.cleaned_data.get('auditor_validation')
        loan_application = LoanApplication.objects.get(id=self.kwargs['pk'])
        loan_application.auditor_validation = auditor_validation
        loan_application.save()

        source_account = loan_application.account
        amount = loan_application.amount
        payment_count = loan_application.payment_count
        total_interest = (payment_count/12) * (14/100) * amount
        total_payment = total_interest + amount

        # trans1 = Transaction(account=source_account, amount=amount, transaction_type='w') TODO

        return super(Auditor_LoanDetailView, self).form_valid(form)

