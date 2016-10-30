from django.conf.urls import url
from finance.views import *

urlpatterns = [
	url(r'^$', front_page, name="front_page"),
	url(r'^charges/', charges_page, name="charges_page"),
]
