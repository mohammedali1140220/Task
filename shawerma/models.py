# -*- coding: utf-8 -*-

import datetime
import django.utils.timezone

from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    pass


class Menu(models.Model):
    name = models.CharField(max_length=100)
    order_type = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name

class View (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu , on_delete=models.CASCADE)

"""
when we make a new order we should make anew history
"""


class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    menu_id=models.ForeignKey(Menu, on_delete=models.CASCADE)
    """in the user_id we have a problem that we add a defult value at the first so we need to modified it"""
    quantity = models.DecimalField(max_digits=8,decimal_places=2)
    address = models.CharField(max_length=100)
    delivery_time = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateTimeField('Enter the date')
    price = models.DecimalField(max_digits=8, decimal_places=2)


class Has(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)


class Make(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

