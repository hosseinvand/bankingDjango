
from django import forms
from django.forms import ModelForm, fields_for_model, Form
from core.models import Customer, Employee, Branch, Account, SystemConfiguration, Manager, Cashier, Jursit, Auditor, \
    BillType, Transaction, Card, Bill, ChequeApplication, Cheque, ChequeIssue




class Block_Account_form(Form):
    button_text = "مسدود کردن حساب"

    account = forms.ModelChoiceField(queryset=Account.objects.filter(is_blocked=False), label='حساب مورد نظر')

    def clean(self):
        cleaned_data = super(Block_Account_form, self).clean()
        return cleaned_data



