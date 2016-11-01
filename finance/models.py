from django.db import models

# Create your models here.


class Account(models.Model):
    _total = models.DecimalField(max_digits=30, decimal_places=2)

    @classmethod
    def create(cls, total):
        account = cls(_total = round(total, 2))
        account.save()
        return account

    def add_charge(self, sum):
        if self._total + sum < 0:
            return

        charge = Charge.create(self, sum)
        charge.save()
        self._total += sum

    def __iter__(self):
        return self.charges.all().__iter__()

    @property
    def total(self):
        return self._total


class Charge(models.Model):
    _value = models.DecimalField(max_digits=10, decimal_places=2)
    _date = models.DateField()

    @property
    def value(self):
        return self._value

    @property
    def date(self):
        return self._date



