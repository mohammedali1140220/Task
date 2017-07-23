from task import settings
from django.test import TestCase
from shawerma.models import Order,User,Menu
from django.db.models import Max,Count,Avg,Sum
from rest_framework.test import APIRequestFactory,RequestsClient,APIClient
from django.contrib.auth.models import User
from rest_framework import status
from django.core.urlresolvers import reverse
"""
class ModelTestCase(TestCase):

    def test_api_can_get_a_user(self):

        menu = Menu.objects.get()
        response2 = self.client.get(
            reverse('detials'),
            kwargs={'pk': menu.id}, format="json"
        )
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertContains(response2, menu)

    def test_api_can_update_user(self):
        
        change_user = {'name':'Something new'}
        res = self.client.put(
            reverse('detials', kwargs = {'pk':user.id}),
            change_user, formate = 'json'
        )
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        :return:
        


        change_menu = {'name': 'Something new'}
        res1 = self.client.put(
            reverse('detials', kwargs={'pk': menu.id}),
            change_menu, formate='json'
        )
        self.assertEqual(res1.status_code, status.HTTP_200_OK)

    def test_api_can_delete_user(self):
        
            user = User.objects.get()
        response = self.client.delete(
            reverse('details' , kwargs={'pk':user.id}),
            format= ' json', follow = True
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        :return:
        

        menu = Menu.objects.get()
        response1 = self.client.delete(
            reverse('details', kwargs={'pk': menu.id}),
            format=' json', follow=True
        )
        self.assertEqual(response1.status_code, status.HTTP_204_NO_CONTENT)

"""
class ViewTestCase(TestCase):
    fixtures = ['fixtures/test.json']

    def test_make_order(self):
        client = APIClient()
        #u = User.objects.filter(username="Ali")
        client.login(username="admin", password="password123")
        Menu.objects.create(name='say', order_type='sandwitch', price='11')
        response = client.get('/shawermaOrder/')
        response = client.post('/shawermaOrder/',{'quantity':1,'address':'Ram','delivery_time':10,'date':'2008-11-11 13:23:44','price':12,'user_id': '1', 'menu_id':'1'},format='json')
        self.assertEqual (response.data,{'menu_id': 1, 'delivery_time': u'10.00', 'user_id': 1, 'price': u'12.00', 'address': u'Ram', 'date': u'2008-11-11T13:23:44Z', u'id': 5, 'quantity': u'1.00'} )
        client.logout()


    def test_get_user_order(self):
        client=APIClient()
        client.login(username="Ali", password="password123")
        query1 = Order.objects.filter(user_id=2)
        response = client.get('/shawermaHistory/2/')
        #self.assertEqual(response.data[0] , query1[0])
        #how can i take the value like date ?
        #this method is true
        client.logout()


    def test_retrive_menu_item(self):
        client = APIClient()
        client.login(username="Ali", password="password123")
        query1= Menu.objects.all()
        response = client.get('/shawerma/')
        #self.assertEqual(response,query1)
        client.logout()


    def test_best_customer(self):
        client = APIClient()
        client.login(username="Ali", password="password123")
        queryset = Order.objects.all().filter(date__year=2017)
        count1 = queryset.values('user_id').annotate(total_price=Sum('price')).order_by('total_price')[:1]
        response = client.get('/shawermaCreateBestCustomer/2017/')
        #self.assertEqual(response,count1)
        client.logout()


    def test_avg_customer(self):
        client = APIClient()
        client.login(username="Ali",password="password123")
        queryset = Order.objects.filter(user_id=2)
        queryset = queryset.values("user_id").annotate(Avg('price'))
        response = client.get('/shawermaCreateAVGCustomer/2/')
        #self.assertEqual(response,queryset)
        client.logout()

    def test_monthly_report_admin(self):
        client = APIClient()
        client.login(username="admin", password="password123")
        queryset = Order.objects.all().filter(date__year=2017)
        queryset = queryset.values('id').aggregate(total_amount=Sum('price'))
        response = client.get('/shawermaCreateMonthlyReport/2017/')
        #self.assertEqual(response,queryset)
        client.logout()
        #it is run

    def test_monthly_report(self):
        client = APIClient()
        client.login(username="Ali", password="password123")
        queryset = Order.objects.all().filter(date__year=2017)
        queryset = queryset.values('id').aggregate(total_amount=Sum('price'))
        response = client.get('/shawermaCreateMonthlyReport/2017/')
        #self.assertEqual(response,queryset)
        client.logout()
        #it is run


    def test_log_in(self):
        Menu.objects.create(name='say', order_type='sandwitch', price='11')
        client= APIClient()
       # user = User.objects.get(username='Ali')
       # client.force_authenticate(user=user)
        response = client.get('/shawermaOrder/')
        response = client.post('/shawermaOrder/',{'quantity':1,'address':'Ram','delivery_time':10,'date':'2008-11-11 13:23:44','price':12,'user_id': '1', 'menu_id':'1'},format='json')
        self.assertNotEqual (response.data,{'menu_id': 1, 'delivery_time': u'10.00', 'user_id': 1, 'price': u'12.00', 'address': u'Ram', 'date': u'2008-11-11T13:23:44Z', u'id': 5, 'quantity': u'1.00'} )
        client.logout()

    #get history for primery key is not exist
    #i dont know what it will return while pk is false
    def test_get_user_order2(self):
        client=APIClient()
        client.login(username="Ali", password="password123")
        query1 = Order.objects.filter(user_id=2)
        response = client.get('/shawermaHistory/10/')
        #self.assertEqual(response.data[0] , query1[0])
        #how can i take the value like date ?
        #this method is true
        client.logout()

    #if customer is not logged in then it will return nothing
    def test_avg_customer1(self):
        client = APIClient()
        response = client.get('/shawermaCreateAVGCustomer/2/')
        #self.assertEqual(response,queryset)
        client.logout()