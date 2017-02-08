from django.forms import ModelForm

from core.models import ChequeIssue, LoanApplication


class Auditor_ChequeDetail_Form(ModelForm):
    class Meta:
        model = ChequeIssue
        fields = ['auditor_validation']
        labels = {
            'auditor_validation': "نظر حسابرس ",
        }

    def clean(self):
        cleaned_data = super(Auditor_ChequeDetail_Form, self).clean()
        # auditor_validation = cleaned_data.get('auditor_validation')  TODO
        # cheque_issue = ChequeIssue.objects.get(id=self.kwargs['pk'])
        # source_account = cheque_issue.cheque.cheque_application.account
        # dest_account = cheque_issue.dest
        # amount = cheque_issue.amount
        #
        # if auditor_validation == "RE":
        #     return cleaned_data
        #
        # if source_account.is_blocked:
        #     self.add_error("cheque_issue", "اکانت مبدا بلاک شده است.")
        # if dest_account.is_blocked:
        #     self.add_error("cheque_issue", "اکانت مقصد بلاک شده است.")
        # if (source_account.balance < 10000 + amount):
        #     self.add_error("cheque_issue", "موجودی حساب مبدا کافی نیست.")

        return cleaned_data


class Auditor_LoanDetail_Form(ModelForm):
    class Meta:
        model = LoanApplication
        fields = ['auditor_validation']
        labels = {
            'auditor_validation': "نظر حسابرس",
        }

    def clean(self):
        cleaned_data = super(Auditor_LoanDetail_Form, self).clean()
        return cleaned_data


