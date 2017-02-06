from django.forms import ModelForm

from core.forms.admin import EmployeeCreateForm
from django import forms

from core.models import Branch, ATM, Maintainer

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

    def __init__(self, data=None, *args, **kwargs):
        super(ATMCreateForm, self).__init__(data)
        self.user = kwargs.get('user')
        branch = self.user.manager.branch
        self.fields['maintainer'].queryset = Maintainer.objects.filter(branch=branch)

    class Meta:
        model = ATM
        fields = ['serial', 'maintainer']
        labels = {
            'serial': "شماره سریال دستگاه",
            'maintainer': 'مسئول دستگاه'
        }

    def clean(self):
        cleaned_data = super(ATMCreateForm, self).clean()
        # validate form data here!
        return cleaned_data

    def save(self, commit=True):
        atm = ATM(branch=self.user.manager.branch, **self.cleaned_data)
        atm.save()
        return atm


class SetMaintainerForATMForm(forms.Form):
    button_text = "انتخاب مسئول"

    atm = forms.ModelChoiceField(None, label='دستگاه')
    maintainer = forms.ModelChoiceField(None, label='مسئول دستگاه خودپرداز')

    def __init__(self, data=None, *args, **kwargs):
        super(SetMaintainerForATMForm, self).__init__(data)
        user = kwargs.get('user')
        branch = user.manager.branch
        print(branch)
        self.fields['maintainer'].queryset = Maintainer.objects.filter(branch=branch)
        self.fields['atm'].queryset = ATM.objects.filter(branch=branch)

    def save(self):
        atm = self.cleaned_data.get('atm', None)
        maintainer = self.cleaned_data.get('maintainer', None)

        print(atm)
        print(maintainer)

        atm.maintainer = maintainer
        atm.save()

        return atm