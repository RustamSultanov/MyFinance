from django.contrib import admin

from .models import Charge, Account, UserProfile

admin.site.register(Account)
admin.site.register(Charge)
admin.site.register(UserProfile)
