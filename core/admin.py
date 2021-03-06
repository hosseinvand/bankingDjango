from django.contrib import admin
from solo.admin import SingletonModelAdmin
from core.models import *
# Register your models here.
admin.site.register(SystemConfiguration,SingletonModelAdmin)
admin.site.register(Manager)
admin.site.register(Auditor)
admin.site.register(Jursit)
admin.site.register(Cashier)
admin.site.register(Branch)
admin.site.register(PaymentOrder)
admin.site.register(Cheque)
admin.site.register(ChequeApplication)
admin.site.register(ChequeIssue)
admin.site.register(Inquiry)
admin.site.register(Loan)
admin.site.register(LoanApplication)
admin.site.register(Bill)
admin.site.register(BillType)
admin.site.register(Transaction)
admin.site.register(TransactionWage)
admin.site.register(CardToCard)
admin.site.register(WithdrawFromATM)
admin.site.register(Card)
admin.site.register(Account)
admin.site.register(Greenback)
admin.site.register(ATM)
admin.site.register(Maintainer)
admin.site.register(Customer)
admin.site.register(Notification)
admin.site.register(PayedBill)
admin.site.register(Contain)
