

from django import forms
from django.forms import ModelForm, fields_for_model, Form
from core.models import Customer, Employee, Branch, Account, SystemConfiguration, Manager, Cashier, Jursit, Auditor, \
    BillType, Transaction, Card, Bill, ChequeApplication, Cheque, ChequeIssue, LoanApplication, PaymentOrder


class Bill_Payment_form(Form):
    button_text = "پرداخت قبض"

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

class Account_Transaction_Form(Form):
    button_text = "نمایش تراکنش های حساب"

    input_account = forms.ModelChoiceField(queryset=Account.objects.all(), label='شماره حساب')

    def clean(self):
        cleaned_data = super(Account_Transaction_Form, self).clean()
        return cleaned_data



class Card_Issuing_form(ModelForm):
    button_text = "صدور کارت"

    class Meta:
        model = Card
        fields = ['account']
        labels = {
            'account': "شماره حساب",
        }

    def clean(self):
        cleaned_data = super(Card_Issuing_form, self).clean()
        account = cleaned_data.get("account")
        if account.is_blocked:
            self.add_error("account", "اکانت شما بلاک شده است.")
        if len(Card.objects.filter(account=account)) > 0:
            self.add_error("account", "برای این حساب کارت صادر شده است.")
        if account.balance < SystemConfiguration.get_solo().card_production_fee + 10000:
            self.add_error("account",  "موجودی حساب کافی نیست.")
        return cleaned_data

    def save(self, commit=True):
        card = Card(**self.cleaned_data)
        account = card.account
        account.balance -= SystemConfiguration.get_solo().card_production_fee
        account.save()
        card.save()
        return card


class Transfer_Money_form(Form):
    button_text = "انتقال وجه"

    source_account = forms.ModelChoiceField(queryset=Account.objects.all(), label='حساب مبدا')
    dest_account = forms.ModelChoiceField(queryset=Account.objects.all(), label='حساب مقصد')
    amount = forms.IntegerField(label='مبلغ')

    def clean(self):
        cleaned_data = super(Transfer_Money_form, self).clean()
        source_account = cleaned_data.get("source_account")
        dest_account = cleaned_data.get("dest_account")
        amount = cleaned_data.get("amount")

        if source_account.is_blocked:
            self.add_error("source_account", "اکانت مبدا بلاک شده است.")
        if dest_account.is_blocked:
            self.add_error("dest_account", "اکانت مقصد بلاک شده است.")
        if source_account.balance < amount + 10000:
            self.add_error("amount", "پول نداری بدبخت!")
        return cleaned_data




class Withdraw_Cash_from_Account_form(ModelForm):
    button_text = "برداشت وجه"

    class Meta:
        model = Transaction
        fields = ['amount', 'account']
        labels = {
            'amount': "مبلغ برداشتی",
            "account": " حساب"
        }

    def clean(self):
        cleaned_data = super(Withdraw_Cash_from_Account_form, self).clean()
        account = cleaned_data.get("account")
        amount = cleaned_data.get("amount")
        if account.is_blocked:
            self.add_error("account", "اکانت شما بلاک شده است.")
        if account.balance < amount + 10000:
            self.add_error("amount", "پول نداری بدبخت!")

        return cleaned_data

        # @transaction.atomic
        # def save(self, commit=True):
        #     transaction_type = 'w'
        #     trans = Transaction( **self.cleaned_data)
        #     # trans.branch = Auditor.objects.get(pk = )
        #     trans.save()
        #
        #     account = Transaction.account
        #     account.balance -= trans.amount
        #
        #     return account


class Add_Cash_to_Account_form(ModelForm):
    button_text = "افزایش موجودی"

    class Meta:
        model = Transaction
        fields = ['amount', 'account']
        labels = {
            'amount': "مبلغ واریزی",
            "account": " حساب"
        }

    def clean(self):
        cleaned_data = super(Add_Cash_to_Account_form, self).clean()
        account = cleaned_data.get("account")
        if account.is_blocked:
            self.add_error("account", "اکانت شما بلاک شده است.")

        return cleaned_data


class Bill_Create_form(ModelForm):
    button_text = "ایجاد قبض"

    class Meta:
        model = Bill
        fields = ['bill_type', 'amount']
        labels = {
            'bill_type': "نوع قبض",
            'amount': "مقدار قبض",
        }

    def clean(self):
        cleaned_data = super(Bill_Create_form, self).clean()
        return cleaned_data

    def save(self, commit=True):
        bill = Bill(**self.cleaned_data)
        bill.save()
        return bill


class Cheque_Application_form(ModelForm):
    button_text = "صدور چک"

    class Meta:
        model = ChequeApplication
        fields = ['account']
        labels = {
            'account': "حساب کاربری",
        }

    def clean(self):
        cleaned_data = super(Cheque_Application_form, self).clean()
        account = cleaned_data.get("account")
        if account.is_blocked:
            self.add_error("account", "اکانت شما بلاک شده است.")
        if account.balance < SystemConfiguration.get_solo().cheque_production_fee + 10000:
            self.add_error("account", "موجودی شما کافی نمی‌باشد.")
        return cleaned_data

    def save(self, commit=True):
        cheque_application = ChequeApplication(**self.cleaned_data)
        cheque_application.save()
        for i in range(0, 10):
            cheque = Cheque(cheque_application=cheque_application)
            cheque.save()
        return cheque_application


class Cheque_Issue_toAccount_form(ModelForm):
    button_text = "وصول چک"

    class Meta:
        model = ChequeIssue
        fields = ['cheque', 'amount', 'dest']
        labels = {
            'cheque': "مشخصات چک ",
            'amount' : "مبلغ چک",
            'dest' : 'حساب مقصد',
        }

    def clean(self):
        cleaned_data = super(Cheque_Issue_toAccount_form, self).clean()
        account = cleaned_data.get("dest")
        if account.is_blocked:
            self.add_error("dest", "اکانت شما بلاک شده است.")
        return cleaned_data

    def save(self, commit=True):
        cheque_issue = ChequeIssue(**self.cleaned_data)
        cheque_issue.save()
        return cheque_issue

class Cheque_Issue_Cash_form(ModelForm):
    button_text = "وصول چک"

    class Meta:
        model = ChequeIssue
        fields = ['cheque', 'amount']
        labels = {
            'cheque': "مشخصات چک ",
            'amount' : "مبلغ چک",
        }

    def clean(self):
        cleaned_data = super(Cheque_Issue_Cash_form, self).clean()
        return cleaned_data

    def save(self, commit=True):
        cheque_issue = ChequeIssue(**self.cleaned_data)
        cheque_issue.save()
        return cheque_issue


class Loan_Request_form(ModelForm):
    button_text = "ثبت درخواست وام"

    class Meta:
        model = LoanApplication
        fields = ['payment_count', 'amount', 'account']
        labels = {
            'payment_count': "تعداد اقسات",
            'amount' : "مبلغ وام",
            'account' : "حساب کاربری مشتری"
        }

    def clean(self):
        cleaned_data = super(Loan_Request_form, self).clean()
        account = cleaned_data.get("account")
        if account.is_blocked:
            self.add_error("account", "اکانت شما بلاک شده است.")
        return cleaned_data

    def save(self, commit=True):
        loan_application = LoanApplication(**self.cleaned_data)
        loan_application.save()
        return loan_application


class Payment_Order_form(ModelForm):
    button_text = "ثبت درخواست حواله های منظم"

    class Meta:
        model = PaymentOrder
        fields = ['account', 'dest', 'amount', 'start_date', 'end_date', 'period_type']
        labels = {
            'account': "حساب مشتری",
            'dest' : "حساب مقصد",
            'amount' : "مقدار انتقالی",
            'start_date': "تاریخ شروع",
            'end_date': "تاریخ پایان",
            'period_type': "نوع زمانی حواله",
        }

    def clean(self):
        cleaned_data = super(Payment_Order_form, self).clean()
        account = cleaned_data.get("account")
        dest_account = cleaned_data.get("dest")
        if account.is_blocked:
            self.add_error("account", "اکانت شما بلاک شده است.")
        if dest_account.is_blocked:
            self.add_error("dest", "اکانت مقصد بلاک شده است.")
        return cleaned_data

    def save(self, commit=True):
        payment_order = PaymentOrder(**self.cleaned_data)
        payment_order.save()
        return payment_order