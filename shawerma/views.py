from __future__ import unicode_literals

from django.db.models import Max,Count,Avg,Sum,F,Value
from django.db.models.functions import TruncMonth
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.response import Response

from .serializers import MonthlyReport,AVGCustomer,ItemSerializers,MenuSerializers,OrderSerializers,HistorySerializers,BestCustomer
from .models import User,MenuItem,Order


class CreateView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuSerializers

class CreateNewOrder(generics.CreateAPIView):
    serializer_class = OrderSerializers
    queryset = Order.objects.all()

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_superuser:
            queryset = Order.objects.all()

            return Response(queryset)
        else:
            return Response(401)

class CreateNewItem(generics.CreateAPIView):
    serializer_class =ItemSerializers


class CreateHistory(generics.ListCreateAPIView):
    queryset = ""
    serializer_class = HistorySerializers
    #i have an error with quantity
    def list(self, request, *args, **kwargs):
        pk1 = self.kwargs['pk']
        queryset = Order.objects.filter(user=pk1).annotate(total=Sum(F('item__quantity') * F('item__menu__price')))
        return Response(HistorySerializers(queryset, many=True).data)


class CreateAVGCustomer(generics.ListCreateAPIView):
    serializer_class = AVGCustomer
    queryset = ""

    def list(self, request, *args, **kwargs):
        pk= self.kwargs['pk']
        return Response(Order.objects.filter(user=pk).annotate(total=Avg(F('item__quantity') * F('item__menu__price'))).aggregate(avg1=Avg('total')).values())


class CreateBestCustomer(generics.ListCreateAPIView):
    serializer_class = BestCustomer
    def list(self, request, *args, **kwargs):
        year = self.kwargs['year']
        return Response(Order.objects.filter(created_date__year = year).annotate(total=Sum(F('item__quantity') * F('item__menu__price'))).values('user_id', 'total').annotate(Count('user_id')).order_by('-total').values('user_id')[0])


class CreateMonthlyReport(generics.ListCreateAPIView):
    serializer_class = MonthlyReport

    def list(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_superuser:
            year = self.kwargs['year']
            queryset = Order.objects.filter(created_date__year=year).annotate(month=TruncMonth('created_date')).values('month').annotate(total=Sum(F('item__quantity') * F('item__menu__price'))).values('month','total')

            return Response(queryset)
        else:
            return Response(401)
