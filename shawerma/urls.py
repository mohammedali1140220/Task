from django.conf.urls import url,include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateView,CreateMonthlyReport,DetialsView,CreateAVGCustomer,CreateNewOrder,DetialsOrderView,CreateHistory,CreateBestCustomer

from . import views

urlpatterns = [
    url(r'shawerma/$',CreateView.as_view(),name="Create"),
    url(r'shawermaOrder/$',CreateNewOrder.as_view(),name="Create order"),
    url(r'shawermaCreateAVGCustomer/(?P<pk>\d+)/$',CreateAVGCustomer.as_view(),name="Create AVG"),
    url(r'^shawermaCreateBestCustomer/(?P<year>\d+)/$',CreateBestCustomer.as_view(), name="Create Best Customer"),
    url(r'^shawermaCreateMonthlyReport/(?P<year>\d+)/$', CreateMonthlyReport.as_view(), name="Create Monthly Report"),
    url(r'shawermaHistory/(?P<pk>\d+)/$',CreateHistory.as_view(),name="Create history"),
]

urlpatterns = format_suffix_patterns(urlpatterns)