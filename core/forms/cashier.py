

from django import forms
from django.forms import ModelForm, fields_for_model, Form
from core.models import Customer, Employee, Branch, Account, SystemConfiguration, Manager, Cashier, Jursit, Auditor, \
    BillType, Transaction, Card, Bill


class Bill_Payment_form(Form):
    account = forms.ModelChoiceField(queryset=Account.objects.all(), label='حساب پرداخت کننده')
    bill = forms.ModelChoiceField(queryset=Bill.objects.filter(paid=False), label='قبض مورد پرداخت')

    def clean(self):
        cleaned_data = super(Bill_Payment_form, self).clean()
        account = cleaned_data.get("account")
        bill = cleaned_data.get("bill")
        amount = bill.amount

        if account.is_blocked:
            self.add_error("account", "اکانت مبدا بلاک شده است.")
        if account.balance < amount + 10000:
            self.add_error("bill.amount", "پول نداری بدبخت!")

        return cleaned_data