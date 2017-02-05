from django.forms import ModelForm

from core.forms.admin import EmployeeCreateForm
from django import forms

from core.models import Branch, ATM

EMPLOYEE_TYPES = (
    ('Cashier', 'صندوق دار'),
    ('Jursit', 'کارشناس حقوقی'),
    ('Auditor', 'حسابرس'),
    ('Maintainer', 'مسئول دستگاه خودپرداز'),
)


class BranchEmployeeCreateForm(EmployeeCreateForm):
    type = forms.ChoiceField(choices=EMPLOYEE_TYPES, label='سمت')

    def __init__(self, data=None, *args, **kwargs):
        super(BranchEmployeeCreateForm, self).__init__(data, *args, **kwargs)
        self.user = kwargs.get('user')
        branch = self.user.manager.branch
        self.fields['branch'].initial = branch
        self.fields['branch'].queryset = Branch.objects.filter(id=branch.id)


class ATMCreateForm(ModelForm):
    button_text = "ایجاد دستگاه"

    class Meta:
        model = ATM
        fields = ['serial', ]
        labels = {
            'serial': "شماره سریال دستگاه",
        }

    def clean(self):
        cleaned_data = super(ATMCreateForm, self).clean()
        # validate form data here!
        return cleaned_data

    def save(self, commit=True):
        atm = ATM(branch=self.user.manager.branch, **self.cleaned_data)
        atm.save()
        return atm
