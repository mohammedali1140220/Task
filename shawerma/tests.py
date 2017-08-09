from __future__ import unicode_literals
import datetime

from django.db.models.functions import TruncMonth
from django.conf import settings
from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models import Max,Count,Avg,Sum,F

from rest_framework.test import APIRequestFactory,RequestsClient,APIClient
from rest_framework import status

from shawerma.models import Order,User,MenuItem


class ViewTestCase(TestCase):
    fixtures = ['fixtures/test.json']

    def test_make_order(self):
        client = APIClient()
        client.login(username="admin", password="password123")
        response = client.post('/shawerma_order/create/',{'address':'Ram'},format='json')
        self.assertEqual (response.data['id'],11)
        client.logout()

    def test_get_user_order(self):
        client=APIClient()
        client.login(username="Ali", password="password123")
        response = client.get('/shawerma-history/2/')
        self.assertEqual(response.data[1]['id'] , 8)
        client.logout()

    def test_retrive_menu_item(self):
        client = APIClient()
        client.login(username="Ali", password="password123")
        response = client.get('/shawerma/')
        self.assertEqual(response.data[0]['id'],1)
        client.logout()

    def test_best_customer(self):
        client = APIClient()
        client.login(username="Ali", password="password123")
        response = client.get('/shawerma-best-customer/2017/')
        self.assertEqual(response.data['user_id'],2)
        client.logout()

    def test_avg_customer(self):
        client = APIClient()
        client.login(username="admin",password="password123")
        queryset = Order.objects.filter(user=2).annotate(total=Avg(F('item__quantity') * F('item__menu__price'))).aggregate(avg1=Avg('total')).values()
        response = client.get('/shawerma-createAVG-customer/2/')
        self.assertEqual(response.data[0],queryset[0])
        client.logout()

    def test_monthly_report_admin(self):
        client = APIClient()
        client.login(username="admin", password="password123")
        queryset = Order.objects.filter(created_date__year=2017).annotate(month=TruncMonth('created_date')).values('month').annotate(total=Sum(F('item__quantity') * F('item__menu__price'))).values('month', 'total')
        response = client.get('/shawerma-monthly-report/2017/')
        self.assertEqual(response.data[0]['total'],738)
        client.logout()
        #it is run

    def test_monthly_report_unauthorized(self):
        client = APIClient()
        client.login(username="Ali", password="password123")
        response = client.get('/shawerma-monthly-report/2017/')
        self.assertEqual(response.data,401)
        client.logout()

    def test_log_in(self):
        client = APIClient()
        response = client.post('/shawerma_order/create/',{'address':'Ram'},format='json')
        #here the client is not logged in and still give me 403
        self.assertEqual (response.status_code,403)
        client.logout()

    def test_get_user_order2(self):
        client=APIClient()
        client.login(username="Ali", password="password123")
        response = client.get('/shawermaHistory/10/')
        self.assertEqual(response.status_code ,404)
        client.logout()

    #if customer is not logged in then it will return nothing
    def test_avg_customer1(self):
        client = APIClient()
        response = client.get('/shawerma-createAVG-customer/2/')
        self.assertEqual(response.status_code,403)
        client.logout()
