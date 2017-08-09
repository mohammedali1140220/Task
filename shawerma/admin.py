# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .models import User,MenuItem,Order,OrderdItem


admin.site.register(User)
admin.site.register(Order)
admin.site.register(MenuItem)
admin.site.register(OrderdItem)
