import decimal
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from rest_framework import generics
from rest_framework.response import Response
from .serializers import UserSerializers,MonthlyReport,AVGCustomer,MenuSerializers,OrderSerializers,HistorySerializers,BestCustomer
from .models import User,Menu,Order
from django.db.models import Max,Count,Avg,Sum

import datetime

class CreateView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializers

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()


class CreateNewOrder(generics.ListCreateAPIView):

    queryset = Order.objects.annotate(max = Max('id')).order_by('max')[:1]
    serializer_class = OrderSerializers

    def perform_create(self, serializer):
        serializer.save()





class CreateHistory(generics.ListCreateAPIView):

    queryset = Order.objects.all()
    serializer_class = HistorySerializers

    def list(self, request, *args, **kwargs):
        pk1 = self.kwargs['pk']
        queryset = Order.objects.filter(user_id=pk1)
        return Response(HistorySerializers(queryset, many=True).data)
    def perform_create(self, serializer):
        serializer.save()


class CreateAVGCustomer(generics.ListCreateAPIView):

    #values('user_id').annotate(avg1=Avg('price')).order_by('avg1')
    serializer_class = AVGCustomer

    def list(self, request, *args, **kwargs):
        pk= self.kwargs['pk']
        queryset = Order.objects.filter(user_id=pk)
        queryset = queryset.values("user_id").annotate(Avg('price'))
        return Response(queryset)

    def perform_create(self, serializer):
        serializer.save()


class CreateBestCustomer(generics.ListCreateAPIView):

    serializer_class = BestCustomer
    def list(self, request, *args, **kwargs):
        year = self.kwargs['year']
        queryset = Order.objects.all().filter(date__year=year)
        count1 = queryset.values('user_id').annotate(total_price = Sum('price')).order_by('total_price')[:1]
        return Response(count1)

    def perform_create(self, serializer):
        serializer.save()


class CreateMonthlyReport(generics.ListCreateAPIView):
    serializer_class = MonthlyReport

    def list(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_superuser:
            year = self.kwargs['year']
            queryset = Order.objects.all().filter(date__year = year)
            queryset = queryset.values('id').aggregate(total_amount = Sum('price'))
            user = self.request.user
            return Response(queryset)
        else:
            return Response('shwerma/login_error.html')

    def perform_create(self, serializer):
        serializer.save()

class DetialsView(generics.RetrieveUpdateDestroyAPIView):
    """
        queryset = User.objects.all()
        serializer_class = UserSerializers
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializers


class DetialsOrderView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers






