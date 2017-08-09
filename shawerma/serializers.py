from __future__ import unicode_literals

from django.db.models import Max,Count,Avg,Sum,F

from rest_framework import serializers

from .models import User,MenuItem,Order,OrderdItem


class ItemSerializers(serializers.ModelSerializer):

    class Meta:
        model = OrderdItem
        fields = "__all__"
        extra_kwargs = {
            'menu': {'write_only': True},
            'order': {'write_only': True},
            'quantity': {'write_only': True},
        }


class MenuSerializers(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ('id', 'name', 'price')
        read_only_fields = ('name','price')

class OrderSerializers(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = ('id','items','created_date','address','total_price')
        read_only_fields = ('user','created_date','total_price')
        extra_kwargs = {
            #'items': {'write_only': True},
            'address':{'write_only':True},
        }
        list_display = ('items',)

    def get_total_price(self, order):
        #order ?!!
        total = OrderdItem.objects.filter(order=order).aggregate(total = Sum(F('quantity')*F('menu__price')))['total']
        return total


class HistorySerializers(serializers.ModelSerializer):
    quantity = serializers.SerializerMethodField()
    items = MenuSerializers(many=True)
    class Meta:
        model = Order
        fields = ('id','created_date','quantity','items')
        read_only_fields = ('created_date','quantity','items',)

    def get_quantity(self,order):
        return ""

class BestCustomer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('id',)


class AVGCustomer (serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id','created_date')
        read_only_fields = ('created_date',)


class MonthlyReport(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id','created_date')
        read_only_fields = ('created_date',)
