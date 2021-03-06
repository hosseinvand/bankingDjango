from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic import TemplateView

from core.forms.atm import LoginATMForm, WithdrawATMForm, CardToCardATMForm


class LoginATM(TemplateView):
    template_name = 'core/atm_login.html'

    def get_context_data(self, **kwargs):
        context = super(LoginATM, self).get_context_data(**kwargs)
        return context


class LoginATM(FormView):
    template_name = 'core/simple_from_with_single_button.html'
    form_class = LoginATMForm

    def get_success_url(self):
        url = reverse_lazy('core:atm_panel', kwargs={'card_number': self.card_number, 'atm': self.atm.id})
        print(url)
        return url

    def form_valid(self, form):
        self.card_number = form.cleaned_data['card_number']
        self.atm = form.cleaned_data['atm']
        return super(LoginATM, self).form_valid(form)


class PanelATM(TemplateView):
    template_name = 'core/atm_panel.html'

    def get_context_data(self, **kwargs):
        context = super(PanelATM, self).get_context_data(**kwargs)
        context.update(self.kwargs)
        return context


class WithdrawATM(FormView):
    template_name = 'core/simple_from_with_single_button.html'
    success_url = reverse_lazy('core:atm_login')
    form_class = WithdrawATMForm

    def get_form_kwargs(self):
        kwargs = super(FormView, self).get_form_kwargs()
        kwargs.update({'atm': self.kwargs.get('atm'), 'card_number': self.kwargs.get('card_number')})
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(WithdrawATM, self).form_valid(form)


class CardToCardATM(FormView):
    template_name = 'core/simple_from_with_single_button.html'
    success_url = reverse_lazy('core:atm_login')
    form_class = CardToCardATMForm

    def get_form_kwargs(self):
        kwargs = super(FormView, self).get_form_kwargs()
        kwargs.update({'atm': self.kwargs.get('atm'), 'card_number': self.kwargs.get('card_number')})
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(CardToCardATM, self).form_valid(form)