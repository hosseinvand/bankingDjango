from django.contrib.auth.models import User
from django.db import models


class ATM(models.Model):
    balance = models.IntegerField()


class ATMGuy(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='atm_guy')
    ATM = models.OneToOneField(ATM, on_delete=models.CASCADE, related_name='atm_guy')


class Greenback(models.Model):
    value = models.IntegerField()


class Card(models.Model):
    cardNumber = models.CharField(max_length=20)
    # TODO FK be hesab


class WithdrawFromATM(models.Model):
    ATM = models.ForeignKey(ATM, on_delete=models.SET_NULL, related_name="withdrawal",null=True)
    Card = models.ForeignKey(Card, on_delete=models.SET_NULL, related_name="withdrawal",null=True)
    volume = models.IntegerField()


class CardToCard(models.Model):
    volume = models.IntegerField()
    FromCard = models.ForeignKey(Card, on_delete=models.SET_NULL, related_name="card_to_card_from",null=True)
    ToCard = models.ForeignKey(Card, on_delete=models.SET_NULL, related_name="card_to_card_to",null=True)


class BillType(models.Model):
    company = models.CharField(max_length=30)
    #TODO FK be hesab


class Bill(models.Model):
    billType = models.ForeignKey(BillType, on_delete=models.CASCADE, related_name="bills")
    total = models.IntegerField()
    #TODO fk to pay transaction


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    social_id = models.CharField(max_length=10, unique=True)
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE)
    EMPLOYEE_TYPES = (
        ('au', 'auditor'),
        ('ca', 'cashier'),
        ('ma', 'manager'),
        ('le', 'legal'),
    )
    type = models.CharField(
        max_length=2, choices=EMPLOYEE_TYPES, default='cashier')


class Branch(models.Model):
    manager = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, related_name='+')
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)


class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birthday = models.DateField(
        verbose_name=None, name=None, auto_now=False, auto_now_add=False)
    father_name = models.CharField(max_length=255)


class SystemModel(models.Model):
    card_production_fee = models.IntegerField( default = 0)
    check_production_fee = models.IntegerField( default = 0)


class Account(models.Model):
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE)
    account_number = models.IntegerField(primary_key=True)
    balance = models.IntegerField(default = 0)
