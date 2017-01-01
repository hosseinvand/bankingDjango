from django.contrib.auth.models import User
from django.db import models


class ATM(models.Model):
    balance = models.IntegerField()


class ATMGuy(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='atm_guy')
    ATM = models.OneToOneField(ATM, on_delete=models.CASCADE, related_name='atm_guy')


class eskenas(models.Model):
    value = models.IntegerField()


class Card(models.Model):
    cardNumber = models.CharField(max_length=20)
    # TODO FK be hesab


class withdrawFromATM(models.Model):
    ATM = models.ForeignKey(ATM, on_delete=models.SET_NULL, related_name="withdrawal")
    Card = models.ForeignKey(Card, on_delete=models.SET_NULL, related_name="withdrawal")
    volume = models.IntegerField()


class CardToCard(models.Model):
    volume = models.IntegerField()
    ATM = models.ForeignKey(ATM, on_delete=models.SET_NULL, related_name="card_to_card")
    FromCard = models.ForeignKey(Card, on_delete=models.SET_NULL, related_name="card_to_card_from")
    ToCard = models.ForeignKey(Card, on_delete=models.SET_NULL, related_name="card_to_card_to")


class BillType(models.Model):
    company = models.CharField(max_length=30)
    #TODO FK be hesab


class bill(models.Model):
    billType = models.ForeignKey(BillType, on_delete=models.CASCADE, related_name="bills")
    total = models.IntegerField()
    #TODO fk to pay transaction

