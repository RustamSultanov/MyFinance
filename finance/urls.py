from finance.views import *
from django.conf.urls import url

urlpatterns = [
    url(r'^$', start_page, name="start_page"),
    url(r'charges/', table_page, name="table_page"),
]