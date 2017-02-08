from uuid import UUID

from django import forms

from core.models import Card, ATM, Contain, Transaction, CardToCard, WithdrawFromATM


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

        card = Card.objects.filter(card_number=card_number).first()
        if card.account.is_blocked:
            self.add_error("card_number", "اکانت این کارت مسدود است.")
            return cleaned_data

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

        if sum > self.card.account.balance + 10000:
            raise forms.ValidationError("موجودی کافی نیست")
            return cleaned_data

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

        trans_w = Transaction(account=self.card.account, amount=sum, transaction_type='w', branch=self.atm.branch)
        trans_w.save()

        withdraw = WithdrawFromATM(ATM=self.atm, card=self.card, amount=sum, transaction=trans_w)
        withdraw.save()

        return


class CardToCardATMForm(forms.Form):
    button_text = "انتقال وجه"
    card_number_to = forms.CharField(max_length=100, label='شماره کارت مقصد')
    amount = forms.IntegerField(label='مبلغ')

    def __init__(self, data=None, *args, **kwargs):
        super(CardToCardATMForm, self).__init__(data)
        self.atm = ATM.objects.get(id=kwargs.get('atm'))
        self.card = Card.objects.get(card_number=kwargs.get('card_number'))

    def clean(self):
        cleaned_data = super(CardToCardATMForm, self).clean()
        card_number = cleaned_data['card_number_to']

        if cleaned_data['amount'] > self.card.account.balance + 10000:
            raise forms.ValidationError("موجودی کافی نیست")
            return cleaned_data

        try:
            uuid_obj = UUID(card_number, version=4)
        except:
            self.add_error("card_number_to", "شماره کارت نامعتبر است.")
            return cleaned_data

        if not Card.objects.filter(card_number=card_number).exists():
            self.add_error("card_number_to", "این کارت وجود ندارد.")
            return cleaned_data

        card = Card.objects.filter(card_number=card_number).first()
        if card.account.is_blocked:
            self.add_error("card_number_to", "اکانت این کارت مسدود است.")
            return cleaned_data
        self.card_to = card

        return cleaned_data

    def save(self):

        source_account = self.card.account
        dest_account = self.card_to.account
        amount = self.cleaned_data.get('amount')

        source_account.balance -= amount
        dest_account.balance += amount
        source_account.save()
        dest_account.save()

        trans_w = Transaction(account=source_account, amount=amount, transaction_type='w', branch=self.atm.branch)
        trans_d = Transaction(account=dest_account, amount=amount, transaction_type='d', branch=self.atm.branch)
        trans_w.save()
        trans_d.save()

        card_to_card = CardToCard(from_card=self.card, to_card=self.card_to, amount=amount, deposit=trans_d, withdraw=trans_w, atm=self.atm)
        card_to_card.save()

        return

