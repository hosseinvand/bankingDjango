# -*- coding: utf-8 -*-

from random import randrange
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms import ModelForm, fields_for_model, TextInput, Select, DateInput, ModelChoiceField
from django import forms
from django.utils.crypto import get_random_string

from core.models import Customer, Employee, Branch, Account,SystemConfiguration


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


class EmployeeCreateForm(ModelForm):

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'sex', 'birth_date', 'birth_place',
                  'social_id', 'address', 'education', 'relationship']
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

    def clean(self):
        cleaned_data = super(EmployeeCreateForm, self).clean()
        # validate form data here!
        return cleaned_data

    def save(self, commit=True):
        first_name = self.cleaned_data.get('first_name', None)
        last_name = self.cleaned_data.get('last_name', None)
        username = get_random_string(length=8)
        password = get_random_string(length=8)
        user = User.objects.create_user(username=username, password=password, first_name=first_name,
                                            last_name=last_name)
        employee = Employee(user=user, **self.cleaned_data)
        return employee


class BranchCreateForm(ModelForm):
    # manager_username = forms.CharField(max_length=32, label="نام کاربری مدیر شعبه")

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
        Branch.save()
        return branch


class CustomerCreateForm(ModelForm):
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
            # 'education': "تحصیلات",
            'email': "آدرس ایمیل",
            'notif_type' : "نوع اطلاع رسانی"
        }

    def clean(self):
        cleaned_data = super(CustomerCreateForm, self).clean()
        # validate form data here!
        return cleaned_data

#    def save(self, commit=True):
#        first_name = self.cleaned_data.get('first_name', None)
#        last_name = self.cleaned_data.get('last_name', None)
#        customer = Customer(**self.cleaned_data)
#        customer.save()
#        employee = Employee(real_owner = customer)
#        employee.save()
#        account_number = employee.account_number

#        return employee


class SystemConfigurationForm(ModelForm):


    def __init__(self, *args, **kwargs):
        super(SystemConfigurationForm, self).__init__(*args, **kwargs)
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
