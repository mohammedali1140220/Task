from rest_framework import serializers
from .models import User,Menu,Order


class UserSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class MenuSerializers(serializers.ModelSerializer):

    class Meta:
        model = Menu
        fields = ('id', 'name', 'order_type', 'price')
        read_only_fields = ('name', 'order_type', 'price')


class OrderSerializers(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class HistorySerializers(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('id','price','date','quantity','menu_id')
        read_only_fields = ('price','date','quantity','menu_id',)


class BestCustomer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('id','date')


class AVGCustomer (serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('id','date','price')
        read_only_fields = ('date','price')

class MonthlyReport(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('id','date','price')
        read_only_fields = ('date','price')