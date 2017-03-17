from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db.models import DateTimeField, CharField, DecimalField, ForeignKey, Model
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(AbstractUser):
    phone = PhoneNumberField(unique=True)
    address = CharField(max_length=100, null=True)


class Account(Model):
    number = CharField(unique=True, max_length=12, verbose_name="Account number", validators=[
        RegexValidator(
            r'^\d+$',
            message="Account number must contains only digits"
        ),
        RegexValidator(
            r'^[1-9]{1}\d{11}$',
            message="Account number must have precisely 12 digits and can not start with 0"
        )
    ])
    user = ForeignKey(UserProfile, related_name='accounts')

    def __str__(self):
        return str(self.number)


class Charge(Model):
    value = DecimalField(max_digits=8, decimal_places=2)
    transactedAt = DateTimeField(default=datetime.today)
    account = ForeignKey(Account)

    def __str__(self):
        return "( " + str(self.transactedAt) + " )" + " " + str(self.value) + " -> " + str(self.account)
