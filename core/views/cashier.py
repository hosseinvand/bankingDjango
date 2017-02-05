

from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import FormView, CreateView
from django.views.generic import ListView
from django.views.generic import TemplateView

from core.forms.cashier import Bill_Payment_form, Account_Transaction_Form, Bill_Create_form, Transfer_Money_form, \
    Add_Cash_to_Account_form, Card_Issuing_form, Withdraw_Cash_from_Account_form, Cheque_Application_form
from core.models import BillType, Card, PayedBill, Bill, ChequeApplication, ChequeIssue
from core.models import Customer, SystemConfiguration, Branch, Account, Transaction
from core.models import Manager, Jursit, Auditor, Cashier





class Bill_Payment_view(FormView):
    template_name = 'core/simple_from_with_single_button.html'
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





class Account_Transactions_View(FormView):
    template_name = 'core/simple_from_with_single_button.html'
    form_class = Account_Transaction_Form

    def get_success_url(self):
        return reverse_lazy('core:account_transactions_select_view', kwargs={"pk": self.request.POST['input_account']})

class Account_Transactions_Selection_View(generic.ListView):
    model =  Transaction
    template_name = 'core/transactions.html'
    context_object_name = 'transaction_list'
    def get_queryset(self):
        return Transaction.objects.filter(account=Account.objects.get(pk=self.kwargs['pk'])).order_by('date', 'time')




class Transfer_Money_view(FormView):
    template_name = 'core/simple_from_with_single_button.html'
    success_url = reverse_lazy('core:cashier_panel')
    form_class = Transfer_Money_form

    @transaction.atomic
    def form_valid(self, form):
        source_account = form.cleaned_data.get('source_account')
        dest_account = form.cleaned_data.get('dest_account')
        amount = form.cleaned_data.get('amount')

        source_account.balance -= amount
        dest_account.balance += amount
        source_account.save()
        dest_account.save()

        trans1 = Transaction(account=source_account, amount=amount, transaction_type='w')
        trans2 = Transaction(account=dest_account, amount=amount, transaction_type='d')
        trans1.cashier = Cashier.objects.get(user__pk=self.request.user.id)
        trans2.cashier = Cashier.objects.get(user__pk=self.request.user.id)

        trans1.branch = trans1.cashier.branch
        trans2.branch = trans2.cashier.branch

        trans1.save()
        trans2.save()

        return super(Transfer_Money_view, self).form_valid(form)


class Add_Cash_To_Account_view(CreateView):
    model = Transaction
    template_name = 'core/simple_from_with_single_button.html'
    success_url = reverse_lazy('core:cashier_panel')
    form_class = Add_Cash_to_Account_form

    @transaction.atomic
    def form_valid(self, form):
        temp_form = form.save(commit=False)
        temp_form.cashier = Cashier.objects.get(user__pk=self.request.user.id)
        temp_form.branch = temp_form.cashier.branch
        temp_form.transaction_type = 'd'
        account = temp_form.account
        account.balance += temp_form.amount
        account.save()
        temp_form.save()
        return super(Add_Cash_To_Account_view, self).form_valid(form)



class Bill_Create_view(CreateView):
    model = Bill
    form_class = Bill_Create_form
    template_name = 'core/simple_from_with_single_button.html'
    success_url = reverse_lazy('core:admin_panel')


class CashierPanel(TemplateView):
    template_name = 'core/cashier_panel.html'



class Card_Issuing_view(SuccessMessageMixin, CreateView):
    model = Card
    template_name = 'core/simple_from_with_single_button.html'
    success_url = reverse_lazy('core:cashier_panel')
    form_class = Card_Issuing_form
    success_message = "شماره کارت صادر شده: " + " %(card_number)s"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            card_number=self.object.card_number
        )



class Withdraw_Cash_from_Account_view(SuccessMessageMixin, CreateView):
    model = Transaction
    template_name = 'core/simple_from_with_single_button.html'
    success_url = reverse_lazy('core:cashier_panel')
    form_class = Withdraw_Cash_from_Account_form

    # success_message = "%(balance)s" + " برابر است با:  " + "%(last_name)s %(first_name)s  "موجودی جدید حساب
    success_message = "موجودی جدید حساب برابر است با:     %(balance)s"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            first_name=self.object.account.real_owner.first_name,
            last_name=self.object.account.real_owner.last_name,
            balance=self.object.account.balance,
        )

    @transaction.atomic
    def form_valid(self, form):
        temp_form = form.save(commit=False)
        temp_form.cashier = Cashier.objects.get(user__pk=self.request.user.id)
        temp_form.branch = temp_form.cashier.branch
        temp_form.transaction_type = 'w'
        account = temp_form.account
        account.balance -= temp_form.amount
        account.save()
        temp_form.save()
        return super(Withdraw_Cash_from_Account_view, self).form_valid(form)

class Cheque_Application_view(CreateView):
    model = ChequeApplication
    template_name = 'core/simple_from_with_single_button.html'
    success_url = reverse_lazy('core:cashier_panel')
    form_class = Cheque_Application_form


class Cheque_Issue_view(CreateView):
    model = ChequeIssue
    template_name = 'core/simple_from_with_single_button.html'
    success_url = reverse_lazy('core:cashier_panel')
    form_class = Cheque_Application_form
