from django.conf.urls import url,include

from rest_framework.urlpatterns import format_suffix_patterns

from .views import CreateView,CreateMonthlyReport,CreateNewItem,CreateAVGCustomer,CreateNewOrder,CreateHistory,CreateBestCustomer

from . import views

urlpatterns = [
    url(r'shawerma/$',CreateView.as_view(),name = "Create"),#done View the menu item
    url(r'shawerma_order/create/$',CreateNewOrder.as_view(),name ="Create order"),
    url(r'shawerma_item/create/$',CreateNewItem.as_view(),name ="Create Item"),
    url(r'shawerma-createAVG-customer/(?P<pk>\d+)/$',CreateAVGCustomer.as_view(),name ="Create AVG"),#done
    url(r'^shawerma-best-customer/(?P<year>\d+)/$',CreateBestCustomer.as_view(), name ="Create Best Customer"),#done
    url(r'^shawerma-monthly-report/(?P<year>\d+)/$', CreateMonthlyReport.as_view(), name ="Create Monthly Report"),
    url(r'shawerma-history/(?P<pk>\d+)/$',CreateHistory.as_view(),name ="Create history"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
