from django import forms
from datetime import date
from django.core.exceptions import ValidationError


class ChargeForm(forms.Form):
    value = forms.DecimalField(label = 'Value', required = True)
    _date = forms.DataField(label = 'Data', required = True)


    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('value')<0:
            if cleaned_data.get('_date') > date.today():
                self.add_error('_date', 'Дата списания не может превышать сегодняшнюю')
        return self