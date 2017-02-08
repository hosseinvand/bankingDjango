
from django import forms
from django.forms import ModelForm, fields_for_model, Form
from core.models import Customer, Employee, Branch, Account, SystemConfiguration, Manager, Cashier, Jursit, Auditor, \
    BillType, Transaction, Card, Bill, ChequeApplication, Cheque, ChequeIssue, Loan, LoanApplication


class Block_Account_form(Form):
    button_text = "مسدود کردن حساب"

    account = forms.ModelChoiceField(queryset=Account.objects.filter(is_blocked=False), label='حساب مورد نظر')

    def clean(self):
        cleaned_data = super(Block_Account_form, self).clean()
        return cleaned_data



class Jursit_ChequeDetail_Form(ModelForm):
    # button_text = "تایید کارشناس"
    # account = forms.ModelChoiceField(queryset=Account.objects.filter(is_blocked=False), label='حساب مورد نظر')
    class Meta:
        model = ChequeIssue
        fields = ['legal_expert_validation']
        labels = {
            'legal_expert_validation': "نظر کارشناس حقوقی",
        }

    def clean(self):
        cleaned_data = super(Jursit_ChequeDetail_Form, self).clean()
        return cleaned_data



class Jursit_LoanDetail_Form(ModelForm):
    # button_text = "تایید کارشناس"
    # account = forms.ModelChoiceField(queryset=Account.objects.filter(is_blocked=False), label='حساب مورد نظر')
    class Meta:
        model = LoanApplication
        fields = ['legal_expert_validation']
        labels = {
            'legal_expert_validation': "نظر کارشناس حقوقی",
        }

    def clean(self):
        cleaned_data = super(Jursit_LoanDetail_Form, self).clean()
        return cleaned_data


