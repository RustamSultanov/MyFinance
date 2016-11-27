from finance.views import *
from django.conf.urls import url

urlpatterns = [
    url(r'^$', accounts, name="accounts_view"),
    url(r'^account/(?P<pk>[0-9]+)/$', account_details, name='account_details'),
]