import datetime

import django.utils.timezone
from django.db.models import Max,Count,Avg,Sum
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

#edited
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    items=models.ManyToManyField(MenuItem , through="OrderdItem")
    address = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '-'.join([str(thing) for thing in self.items.all()])

class OrderdItem(models.Model):
    menu = models.ForeignKey(MenuItem,on_delete=models.CASCADE,related_name='item')
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='item')
    quantity = models.IntegerField();
