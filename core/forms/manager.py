from core.forms.admin import EmployeeCreateForm
from django import forms

from core.models import Branch

EMPLOYEE_TYPES = (
    ('Cashier', 'صندوق دار'),
    ('Jursit', 'کارشناس حقوقی'),
    ('Auditor', 'حسابرس'),
)


class BranchEmployeeCreateForm(EmployeeCreateForm):
    type = forms.ChoiceField(choices=EMPLOYEE_TYPES, label='سمت')

    def __init__(self, data=None, *args, **kwargs):
        super(BranchEmployeeCreateForm, self).__init__(data, *args, **kwargs)
        self.user = kwargs.get('user')
        # TODO use branch of current user
        self.fields['branch'].initial = Branch.objects.all()[0]
        self.fields['branch'].queryset = Branch.objects.all()
