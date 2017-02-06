from django import forms

from core.models import ATM, Greenback, Contain


class SetGreenbackForATMForm(forms.Form):
    button_text = "ثبت تغییرات"

    atm = forms.ModelChoiceField(None, label='دستگاه')

    def __init__(self, data=None, *args, **kwargs):
        super(SetGreenbackForATMForm, self).__init__(data)
        user = kwargs.get('user')
        self.fields['atm'].queryset = ATM.objects.filter(maintainer=user.maintainer)
        for greenback in Greenback.objects.all():
            self.fields[str(greenback.id)] = forms.IntegerField(label=str(greenback.value))

    def save(self):
        atm = self.cleaned_data.get('atm', None)

        for greenback in Greenback.objects.all():
            count = self.cleaned_data.get(str(greenback.id), 0)
            contain = Contain.objects.filter(greenback=greenback, atm=atm).first()
            if contain:
                contain.count = count
                contain.save()
            else:
                Contain.objects.create(greenback=greenback, atm=atm, count=count)

        atm.save()

        return atm