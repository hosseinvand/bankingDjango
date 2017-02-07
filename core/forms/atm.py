from uuid import UUID

from django import forms

from core.models import Card


class LoginATMForm(forms.Form):
    button_text = "ورود"
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
