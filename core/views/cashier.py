

from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import FormView, CreateView
from django.views.generic import ListView
from django.views.generic import TemplateView

from core.forms.admin import BillTypeCreateForm, \
    Withdraw_Cash_from_Account_form, Add_Cash_to_Account_form, Card_Issuing_form, Transfer_Money_form, \
    Account_Transaction_Form
from core.forms.cashier import Bill_Payment_form
from core.models import BillType, Card, PayedBill
from core.models import Customer, SystemConfiguration, Branch, Account, Transaction
from core.models import Manager, Jursit, Auditor, Cashier





class Bill_Payment_view(FormView):
    template_name = 'core/Bill_payment.html'
    success_url = reverse_lazy('core:cashier_panel')
    form_class = Bill_Payment_form

    @transaction.atomic
    def form_valid(self, form):
        account = form.cleaned_data.get('account')
        bill = form.cleaned_data.get('bill')

        account.balance -= bill.amount
        account.save()

        bill.paid = True
        bill.save()

        trans = Transaction(account=account, amount=bill.amount, transaction_type='w')
        trans.cashier = Cashier.objects.get(user__pk=self.request.user.id)
        trans.branch = trans.cashier.branch
        trans.save()

        payedbill = PayedBill(payment=trans, bill = bill)
        payedbill.save()

        return super(Bill_Payment_view, self).form_valid(form)
