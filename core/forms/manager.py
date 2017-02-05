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
        branch = self.user.manager.branch
        self.fields['branch'].initial = branch
        self.fields['branch'].queryset = Branch.objects.filter(id=branch.id)
