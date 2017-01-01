from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
