from uuid import UUID

from django import forms

from core.models import Card, ATM, Contain


class LoginATMForm(forms.Form):
    button_text = "ورود"
    atm = forms.ModelChoiceField(ATM.objects.all(), label='دستگاه')
    card_number = forms.CharField(max_length=100, label='شماره کارت')

    def clean(self):
        cleaned_data = super(LoginATMForm, self).clean()
        card_number = cleaned_data.get("card_number")

        try:
            uuid_obj = UUID(card_number, version=4)
        except:
            self.add_error("card_number", "شماره کارت نامعتبر است.")
            return cleaned_data

        if not Card.objects.filter(card_number=card_number).exists():
            self.add_error("card_number", "این کارت وجود ندارد.")
        return cleaned_data


class WithdrawATMForm(forms.Form):
    button_text = "برداشت وجه"

    def __init__(self, data=None, *args, **kwargs):
        super(WithdrawATMForm, self).__init__(data)
        self.atm = ATM.objects.get(id=kwargs.get('atm'))
        self.card = Card.objects.get(card_number=kwargs.get('card_number'))
        for contain in Contain.objects.filter(atm=self.atm):
            self.fields[str(contain.greenback.id)] = forms.IntegerField(label=str(contain.greenback.value),
                                                                        help_text='{} {}'.format('تعداد اسکناس موجود:', contain.count))

    def clean(self):
        cleaned_data = super(WithdrawATMForm, self).clean()
        sum = 0

        for contain in Contain.objects.filter(atm=self.atm):
            if int(cleaned_data[str(contain.greenback.id)]) > contain.count:
                self.add_error(str(contain.greenback.id), "اسکناس کافی وجود ندارد.")
                return
            else:
                sum += int(cleaned_data[str(contain.greenback.id)])

        if sum > self.card.account.balance:
            raise forms.ValidationError("موجودی کافی نیست")

        return cleaned_data

    def save(self):
        sum = 0

        for contain in Contain.objects.filter(atm=self.atm):
            sum += int(self.cleaned_data[str(contain.greenback.id)])
            contain.count -= self.cleaned_data[str(contain.greenback.id)]
            contain.save()

        account = self.card.account
        account.balance -= sum
        account.save()
        return
