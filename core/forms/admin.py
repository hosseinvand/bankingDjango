# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms import ModelForm, fields_for_model, Form
from django.utils.crypto import get_random_string

from core.models import Customer, Employee, Branch, Account, SystemConfiguration, Manager, Cashier, Jursit, Auditor, \
    BillType, Transaction, Card, Bill


class LoginForm(ModelForm):
    username = fields_for_model(User)['username']
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Employee
        fields = []

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        try:
            User.objects.get(username=cleaned_data.get("username"))
        except User.DoesNotExist:
            raise forms.ValidationError('Username "%s" Does not exist.' % cleaned_data.get("username"))
        password = self.cleaned_data.get('password')
        username = self.cleaned_data.get('username')
        if not password or len(password) < 1:
            raise forms.ValidationError("password invalid")

        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("user is shasgool")
        return cleaned_data


EMPLOYEE_TYPES = (
    ('Manager', 'مدیر شعبه'),
    ('Cashier', 'صندوق دار'),
    ('Jursit', 'کارشناس حقوقی'),
    ('Auditor', 'حسابرس'),
)


class EmployeeCreateForm(Form):
    button_text = "ایجاد کارمند"
    type = forms.ChoiceField(choices=EMPLOYEE_TYPES, label='سمت')

    labels = {
        'first_name': "نام",
        'last_name': "نام خانوادگی",
        'sex': "جنسیت",
        'birth_date': "تاریخ تولد",
        'birth_place': "محل تولد",
        'social_id': "کد ملی",
        'address': "آدرس",
        'education': "تحصیلات",
        'relationship': "وضعیت تاهل",
        'branch': 'شعبه'
    }

    def __init__(self, data=None, *args, **kwargs):
        super(EmployeeCreateForm, self).__init__(data)
        self.fields.update(fields_for_model(Employee, labels=self.labels))
        del self.fields['user']

    def clean(self):
        cleaned_data = super(EmployeeCreateForm, self).clean()
        print('cleaned_data is: ', cleaned_data)
        return cleaned_data

    def save(self):
        first_name = self.cleaned_data.get('first_name', None)
        last_name = self.cleaned_data.get('last_name', None)
        username = get_random_string(length=8)
        password = get_random_string(length=8)
        user = User.objects.create_user(username=username, password=password, first_name=first_name,
                                        last_name=last_name)
        model = {
            'Manager': Manager,
            'Cashier': Cashier,
            'Jursit': Jursit,
            'Auditor': Auditor
        }[self.cleaned_data.get('type')]
        del self.cleaned_data['type']

        employee = model(user=user, **self.cleaned_data)
        employee.save()

        return employee


class BranchCreateForm(ModelForm):
    button_text = "ایجاد شعبه"

    class Meta:
        model = Branch
        fields = ['name', 'address']
        labels = {
            'name': "نام شعبه",
            'address': "آدرس شعبه"
        }

    def clean(self):
        cleaned_data = super(BranchCreateForm, self).clean()
        # validate form data here!
        return cleaned_data

    def save(self, commit=True):
        branch = Branch(**self.cleaned_data)
        branch.save()
        return branch


class BillTypeCreateForm(ModelForm):
    button_text = "ایجاد قبض"

    class Meta:
        model = BillType
        fields = ['company', 'account']
        labels = {
            'company': "نام شرکت",
            'account': "حساب بانکی مرتبط",
        }

    def clean(self):
        cleaned_data = super(BillTypeCreateForm, self).clean()
        # validate form data here!
        return cleaned_data

    def save(self, commit=True):
        billType = BillType(**self.cleaned_data)
        billType.save()
        return billType


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


class AccountCreateForm(ModelForm):
    button_text = "ایجاد حساب"

    class Meta:
        model = Account
        fields = ['user_type', 'real_owner']
        labels = {
            'user_type': "نوع کاربر",
            "real_owner": "صاحب حساب"
        }

    def clean(self):
        cleaned_data = super(AccountCreateForm, self).clean()
        # validate form data here!
        return cleaned_data

    def save(self, commit=True):
        account = Account(**self.cleaned_data)
        account.save()
        account_number = account.account_number
        return account


class Withdraw_Cash_from_Account_form(ModelForm):
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


class CustomerCreateForm(ModelForm):
    button_text = "ایجاد مشتری"

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'sex', 'birthday', 'father_name',
                  'social_id', 'phone_number', 'email', 'notif_type']
        labels = {
            'first_name': "نام",
            'last_name': "نام خانوادگی",
            'sex': "جنسیت",
            'birthday': "تاریخ تولد",
            'father_name': "نام پدر",
            'social_id': "شماره ملی",
            'phone_number': "شماره تلفن",
            # 'address': "آدرس",
            'email': "آدرس ایمیل",
            'notif_type': "نوع اطلاع رسانی"
        }

    def clean(self):
        cleaned_data = super(CustomerCreateForm, self).clean()
        # validate form data here!
        return cleaned_data

    def save(self, commit=True):
        customer = Customer(**self.cleaned_data)
        customer.save()
        return customer


class Card_Issuing_form(ModelForm):
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
        # if account.balance < 10000 + SystemConfiguration.get_deferred_fields["card_production_fee"]:
        #     self.add_error("account", "موجودی حساب کافی نیست.")

        return cleaned_data

    def save(self, commit=True):
        card = Card(**self.cleaned_data)
        # account = card.account
        # account.balance -= SystemConfiguration.card_production_fee
        # account.save()
        card.save()
        return card


class Account_Transaction_Form(Form):
    input_account = forms.ModelChoiceField(queryset=Account.objects.all(), label='شماره حساب')
    def clean(self):
        cleaned_data = super(Account_Transaction_Form, self).clean()
        return cleaned_data


class Transfer_Money_form(Form):
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





class SystemConfigurationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SystemConfigurationForm, self).__init__(*args, **kwargs)
        print(len(SystemConfiguration.objects.all()))
        instance = SystemConfiguration.objects.get()

        self.fields['card_production_fee'].initial = str(instance.card_production_fee)
        self.fields['cheque_production_fee'].initial = str(instance.cheque_production_fee)
        self.fields['sms_notif_fee'].initial = str(instance.sms_notif_fee)
        self.fields['card_to_card_fee'].initial = str(instance.card_to_card_fee)
        self.fields['transactio_fee'].initial = str(instance.transactio_fee)
        self.fields['atm_min_money'].initial = str(instance.atm_min_money)
        self.fields['loan_interest'].initial = str(instance.loan_interest)
        self.fields['deposit_yearly_interest'].initial = str(instance.deposit_yearly_interest)

    class Meta:
        model = SystemConfiguration
        fields = [
            'card_production_fee',
            'cheque_production_fee',
            'sms_notif_fee',
            'card_to_card_fee',
            'transactio_fee',
            'atm_min_money',
            'loan_interest',
            'deposit_yearly_interest',
        ]
        labels = {
            'card_production_fee': "هزینه‌ی صدور کارت",
            'cheque_production_fee': "هزینه‌ی صدور چک",
            'sms_notif_fee': "هزینه‌ی فعال‌سازی اعلام پیامک",
            'card_to_card_fee': "هزینه‌ی کارت به کارت",
            'transactio_fee': "هزینه‌ی تراکنش",
            'atm_min_money': "مقدار کمینه‌ی پول موجود در خودپرداز",
            'loan_interest': "بهره‌ی وام",
            'deposit_yearly_interest': "بهره‌ی حساب سالیانه",
        }

    def save(self, commit=True):
        instance = SystemConfiguration(**self.cleaned_data)
        instance.save()
        return instance
