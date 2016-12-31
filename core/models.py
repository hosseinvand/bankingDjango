from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    social_id = models.CharField(max_length=10)
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE)

class Branch(models.Model):
    manager=models.ForeignKey(
        Employee, on_delete = models.SET_NULL, null = True, related_name='+')
    name=models.CharField(max_length = 255)
    address=models.CharField(max_length = 255)
