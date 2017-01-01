from django.contrib.auth.models import User
from django.db import models


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
        Maintainer, on_delete=models.SET_NULL, related_name="atm_set", null=True)


class Greenback(models.Model):
    value = models.IntegerField()


class Account(models.Model):
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE)
    account_number = models.IntegerField(primary_key=True)
    balance = models.IntegerField(default=0)


class Card(models.Model):
    card_number = models.CharField(
        max_length=20, unique=True, primary_key=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)


class WithdrawFromATM(models.Model):
    ATM = models.ForeignKey(ATM, on_delete=models.SET_NULL,
                            related_name="withdrawal", null=True)
    card = models.ForeignKey(
        Card, on_delete=models.SET_NULL, related_name="withdrawal", null=True)
    volume = models.IntegerField()


class CardToCard(models.Model):
    volume = models.IntegerField()
    from_card = models.ForeignKey(
        Card, on_delete=models.SET_NULL, related_name="card_to_card_from_set", null=True)
    to_card = models.ForeignKey(
        Card, on_delete=models.SET_NULL, related_name="card_to_card_to_set", null=True)


class BillType(models.Model):
    company = models.CharField(max_length=30)
    # TODO FK be hesab


class Bill(models.Model):
    bill_type = models.ForeignKey(
        BillType, on_delete=models.CASCADE, related_name="bills")
    total = models.IntegerField()
    # TODO fk to pay transaction


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    social_id = models.CharField(max_length=10, unique=True)
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE, related_name='+')

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
        Manager, on_delete=models.SET_NULL, null=True, related_name='+')
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)


class System(models.Model):
    card_production_fee = models.IntegerField(default=0)
    check_production_fee = models.IntegerField(default=0)


class LoanApplication(models.Model):
    balance = models.BigIntegerField()
    payment_count = models.IntegerField()
    legal_expert_confirmation = models.BooleanField(default=False)
    auditor_confirmation = models.BooleanField(default=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)


class Loan(models.Model):
    remaining_payment = models.IntegerField()
    interest = models.FloatField()
    loan_application = models.OneToOneField(
        LoanApplication, on_delete=models.CASCADE)
