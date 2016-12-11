from django.contrib import admin

from .models import Charge, Account

admin.site.register(Account)
admin.site.register(Charge)
