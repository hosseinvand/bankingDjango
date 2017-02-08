# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Sum
from django.forms import ModelForm, fields_for_model, Form
from django.utils.crypto import get_random_string
from graphos.renderers import morris
from graphos.sources.simple import SimpleDataSource

from core.models import Customer, Employee, Branch, Account, SystemConfiguration, Manager, Cashier, Jursit, Auditor, \
    BillType, Transaction, Card, Bill, Maintainer, Greenback, CardToCard


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
        # password = get_random_string(length=8)
        password = username
        user = User.objects.create_user(username=username, password=password, first_name=first_name,
                                        last_name=last_name)
        model = {
            'Manager': Manager,
            'Cashier': Cashier,
            'Jursit': Jursit,
            'Auditor': Auditor,
            'Maintainer': Maintainer
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

class GreenbackCreateForm(ModelForm):
    button_text = "ایجاد اسکناس"

    class Meta:
        model = Greenback
        fields = ['value']
        labels = {
            'value': "ارزش اسکناس",
        }

    def clean(self):
        cleaned_data = super(GreenbackCreateForm, self).clean()
        # validate form data here!
        return cleaned_data

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



class SystemConfigurationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SystemConfigurationForm, self).__init__(*args, **kwargs)
        print(len(SystemConfiguration.objects.all()))
        instance = SystemConfiguration.objects.get()

        self.fields['card_production_fee'].initial = str(instance.card_production_fee)
        self.fields['cheque_production_fee'].initial = str(instance.cheque_production_fee)
        self.fields['sms_notif_fee'].initial = str(instance.sms_notif_fee)
        self.fields['card_to_card_fee'].initial = str(instance.card_to_card_fee)
        self.fields['transaction_fee'].initial = str(instance.transaction_fee)
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
            'transaction_fee',
            'atm_min_money',
            'loan_interest',
            'deposit_yearly_interest',
        ]
        labels = {
            'card_production_fee': "هزینه‌ی صدور کارت",
            'cheque_production_fee': "هزینه‌ی صدور چک",
            'sms_notif_fee': "هزینه‌ی فعال‌سازی اعلام پیامک",
            'card_to_card_fee': "هزینه‌ی کارت به کارت",
            'transaction_fee': "هزینه‌ی تراکنش",
            'atm_min_money': "مقدار کمینه‌ی پول موجود در خودپرداز",
            'loan_interest': "بهره‌ی وام",
            'deposit_yearly_interest': "بهره‌ی حساب سالیانه",
        }

    def save(self, commit=True):
        instance = SystemConfiguration(**self.cleaned_data)
        instance.save()
        return instance

REPORT_PERIOD = (
    ('Day', 'روز'),
    ('Month', 'ماه'),
    ('Year', 'سال'),
)

REPORT_TYPES = (
    ('COUNT', 'بر اساس تعداد عملیات'),
    ('VOLUME', 'بر اساس حجم نقدینگی')
)

REPORT_DOMAIN = (
    ('ALL', 'کل سامانه'),
    ('PART', 'به تفکیک شعب')
)

class ReportForm(forms.Form):
    button_text = "ایجاد گزارش"

    period = forms.ChoiceField(choices=REPORT_PERIOD, label='واحد زمانی')
    type = forms.ChoiceField(choices=REPORT_TYPES, label='مورد گزارش')
    domain = forms.ChoiceField(choices=REPORT_DOMAIN, label='دامنه گزارش')
    begin_date = forms.DateField(label='شروع')
    end_date = forms.DateField(label='پایان')

    branches = forms.ModelMultipleChoiceField(Branch.objects.all(), label='انتخاب شعب', required=False)

    def clean(self):
        cleaned_data = super(ReportForm, self).clean()
        if cleaned_data["end_date"] < cleaned_data["begin_date"]:
            raise forms.ValidationError("تاریخ ورودی نامعتبر است.")
            return cleaned_data
        return cleaned_data

    def save(self):
        begin_date = self.cleaned_data["begin_date"]
        end_date = self.cleaned_data["end_date"]
        period = self.cleaned_data["period"]
        type = self.cleaned_data["type"]
        domain = self.cleaned_data["domain"]
        branches = self.cleaned_data["branches"]

        years = 1 if period == "Year" else 0
        months = 1 if period == "Month" else 0
        days = 1 if period == "Day" else 0

        dates = []
        index_date = begin_date
        while index_date < end_date:
            dates.append(index_date)
            index_date = index_date + relativedelta(years=years, months=months, days=days)
        dates.append(end_date)

        if type == "COUNT":
            meta = ['تاریخ', 'تعداد واریز', 'تعداد برداشت', 'تعداد کارت به کارت']
            datas = [meta]
            if domain == "ALL":
                for i in range(len(dates) - 1):
                    beg = dates[i]
                    end = dates[i+1]
                    row = [beg.strftime("%Y-%m-%d"),
                           Transaction.objects.filter(date__gte=beg, date__lt=end, transaction_type="d").count(),
                           Transaction.objects.filter(date__gte=beg, date__lt=end, transaction_type="w").count(),
                           CardToCard.objects.filter(deposit__date__gte=beg, deposit__date__lt=end).count()]
                    datas.append(row)
                simple_data_source = SimpleDataSource(data=datas)
                bar_chart = morris.BarChart(simple_data_source)
                return [{'name': 'کل سامانه', 'chart': bar_chart}]
            else:
                charts = []
                for branch in branches:
                    for i in range(len(dates) - 1):
                        beg = dates[i]
                        end = dates[i + 1]
                        row = [beg.strftime("%Y-%m-%d"),
                               Transaction.objects.filter(date__gte=beg, date__lt=end, transaction_type="d", branch=branch).count(),
                               Transaction.objects.filter(date__gte=beg, date__lt=end, transaction_type="w", branch=branch).count(),
                               CardToCard.objects.filter(deposit__date__gte=beg, deposit__date__lt=end, deposit__branch=branch).count()]
                        datas.append(row)
                    simple_data_source = SimpleDataSource(data=datas)
                    bar_chart = morris.BarChart(simple_data_source)
                    charts.append({'name': branch.name, 'chart': bar_chart})
                return charts

        else:
            meta = ['تاریخ', 'حجم واریز', 'حجم برداشت']
            datas = [meta]
            if domain == "ALL":
                for i in range(len(dates) - 1):
                    beg = dates[i]
                    end = dates[i + 1]
                    row = [beg.strftime("%Y-%m-%d"),
                           Transaction.objects.filter(date__gte=beg, date__lt=end, transaction_type="d").aggregate(Sum('amount'))['amount__sum'],
                           Transaction.objects.filter(date__gte=beg, date__lt=end, transaction_type="w").aggregate(Sum('amount'))['amount__sum'],]
                    datas.append(row)
                simple_data_source = SimpleDataSource(data=datas)
                bar_chart = morris.BarChart(simple_data_source)
                return [{'name': 'کل سامانه', 'chart': bar_chart}]
            else:
                charts = []
                for branch in branches:
                    for i in range(len(dates) - 1):
                        beg = dates[i]
                        end = dates[i + 1]
                        row = [beg.strftime("%Y-%m-%d"),
                               Transaction.objects.filter(date__gte=beg, date__lt=end, transaction_type="d",
                                                          branch=branch).aggregate(Sum('amount'))['amount__sum'],
                               Transaction.objects.filter(date__gte=beg, date__lt=end, transaction_type="w",
                                                          branch=branch).aggregate(Sum('amount'))['amount__sum'],]
                        datas.append(row)
                    simple_data_source = SimpleDataSource(data=datas)
                    bar_chart = morris.BarChart(simple_data_source)
                    charts.append({'name': branch.name, 'chart': bar_chart})
                return charts

