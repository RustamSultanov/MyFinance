from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.db import models


class UserProfile(AbstractUser):
    phone = models.CharField(max_length=11, unique=True)
    address = models.CharField(max_length=100, null=True)


class Account(models.Model):
    number = models.CharField(primary_key=True, max_length=12, verbose_name="Account number", validators=[
        RegexValidator(
            r'^\d+$',
            message="Account number must contains only digits"
        ),
        RegexValidator(
            r'^[1-9]{1}\d{11}$',
            message="Account number must have precisely 12 digits and can not start with 0"
        )
    ])
    user = models.ForeignKey(UserProfile, related_name='accounts')

    def __str__(self):
        return str(self.number)

    def get_absolute_url(self):
        return reverse('finances:account', args=[str(self.number)])


class Charge(models.Model):
    value = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateField(default=datetime.today)
    account = models.ForeignKey(Account)

    def __str__(self):
        return "( " + str(self.date) + " )" + " " + str(self.value) + " -> " + str(self.account)

    def get_absolute_url(self):
        return reverse("finances:account", kwargs={"number": self.account})
