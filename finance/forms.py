from django import forms
from datetime import date
from .models import Charge, Account
from django.core.exceptions import ValidationError


class ChargeForm(forms.ModelForm):
    _value = forms.DecimalField(label = 'Value', required = True)
    _date = forms.DateField(label = 'Date', required = True)

    class Meta:
        model = Charge
        fields = ("_date", "_value")


class AccountForm(forms.ModelForm):
    _total = forms.DecimalField(label='Начальное состояние', required = True)
    name = forms.CharField(label='Имя счета', max_length=20)
    class Meta:
        model = Account
        fields = ("_total", "name")