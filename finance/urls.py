from django.conf.urls import url
from finance.views import front_page, charges_page

urlpatterns = [
	url(r'^$', front_page),
	url(r'^charges/$', charges_page),
]
