from django.contrib.auth.models import User
from django.db import models


class System(models.Model):
    card_production_fee = models.IntegerField(default=0)
    check_production_fee = models.IntegerField(default=0)


class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birthday = models.DateField()
    father_name = models.CharField(max_length=255)


class Maintainer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)


class ATM(models.Model):
    balance = models.IntegerField()
    maintainer = models.ForeignKey(
        Maintainer, on_delete=models.SET_NULL,
        related_name="atm_set", null=True)


class Greenback(models.Model):
    value = models.IntegerField()


class Account(models.Model):
    owner = models.ForeignKey(Customer, on_delete=models.PROTECT)
    account_number = models.IntegerField(primary_key=True)
    balance = models.IntegerField(default=0)
    is_blocked = models.BooleanField(default=False)


class Card(models.Model):
    card_number = models.CharField(
        max_length=20, unique=True, primary_key=True)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)


class WithdrawFromATM(models.Model):
    ATM = models.ForeignKey(ATM, on_delete=models.SET_NULL,
                            related_name="withdrawal", null=True)
    card = models.ForeignKey(
        Card, on_delete=models.PROTECT, related_name="withdrawal", null=True)
    volume = models.IntegerField()


class CardToCard(models.Model):
    volume = models.IntegerField()

    from_card = models.ForeignKey(
        Card, on_delete=models.PROTECT, related_name="from_card", null=True)

    to_card = models.ForeignKey(
        Card, on_delete=models.PROTECT, related_name="to_card", null=True)

    atm = models.ForeignKey(ATM, on_delete=models.SET_NULL,
                            related_name="card_to_card", null=True)


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    social_id = models.CharField(max_length=10, unique=True)
    branch = models.ForeignKey(
        'Branch', on_delete=models.CASCADE, related_name='+')

    class Meta:
        abstract = True


class Manager(Employee):

    def __str__(self):
        return "Manager: " + first_name + " " + last_name


class Auditor(Employee):

    def __str__(self):
        return "Manager: " + first_name + " " + last_name


class Cashier(Employee):

    def __str__(self):
        return "Manager: " + first_name + " " + last_name


class Jursit(Employee):

    def __str__(self):
        return "Manager: " + first_name + " " + last_name


class Branch(models.Model):
    manager = models.ForeignKey(
        Manager, on_delete=models.PROTECT, null=True, related_name='+')
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)


class Transaction(models.Model):
    amount = models.IntegerField()
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    cashier = models.ForeignKey(
        Auditor, on_delete=models.SET_NULL,null =True, related_name='transactions')

    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    wage_transaction = models.ForeignKey(
        'self', on_delete=models.PROTECT, related_name='+')
    WITHDRAW = 'w'
    DEPOSIT = 'd'
    transaction_types = (
        (WITHDRAW, 'withdraw'),
        (DEPOSIT, 'deposit'),
    )

    transaction_type = models.CharField(
        max_length=1, choices=transaction_types, db_column='type')

    # TODO: why there should be a foreign key to payment orders


class Transfer(models.Model):
    withdraw = models.ForeignKey(
        Transaction, on_delete=models.PROTECT, related_name='+')
    deposit = models.ForeignKey(
        Transaction, on_delete=models.PROTECT, related_name='+')



class BillType(models.Model):
    company = models.CharField(max_length=30)
    account = models.ForeignKey(
        Account, on_delete=models.PROTECT, related_name="bill", null=True)


class Bill(models.Model):
    bill_type = models.ForeignKey(
        BillType, on_delete=models.PROTECT, related_name="bills")
    amount = models.IntegerField()
    payment = models.ForeignKey(
        Transfer, on_delete=models.PROTECT, related_name='+')

class LoanApplication(models.Model):
    balance = models.BigIntegerField()
    payment_count = models.IntegerField()
    legal_expert_confirmation = models.BooleanField(default=False)
    auditor_confirmation = models.BooleanField(default=False)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)


class Loan(models.Model):
    remaining_payment = models.IntegerField()
    interest = models.FloatField()
    loan_application = models.ForeignKey(
        LoanApplication, on_delete=models.PROTECT)


class Inquiry(models.Model):
    UNKNOWN = 'NA'
    ACCEPT = 'AC'
    REJECT = 'RE'
    statuses = (
        (UNKNOWN, 'unknown'),
        (ACCEPT, 'accepted'),
        (REJECT, 'rejected'),
    )
    status = models.CharField(
        max_length=2, choices=statuses, default=UNKNOWN)


class Cheque(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.PROTECT, related_name="cheques")


class PaymentOrder(models.Model):  # NOTE: i don't know what is english for "havale"
    account = models.ForeignKey(
        Account, on_delete=models.PROTECT, related_name="payment_orders")
    amount = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
