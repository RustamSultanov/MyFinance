from django.shortcuts import render
from datetime import date
from decimal import Decimal
from .models import Account, Charge
from random import randint


def start_page(request):
    return render(request, 'finance/start_page.html',  {})


def table_page(request):
    transactions = []
    for i in range(15):
        _date, value = random_transactions().__next__()
        charge = Charge.objects.create(_value = value, _date=_date)
        charge.save()
        transactions.append(charge)

    return render(request, 'finance/table_page.html', {"charges":transactions})


def random_transactions( ):
    today = date.today( )
    start_date = today.replace(month=1, day=1).toordinal()
    end_date = today.toordinal()
    while True:
        start_date = randint(start_date, end_date)
        random_date = date.fromordinal(start_date)
        if random_date >= today:
            break
        random_value = randint(-10000, 10000), randint(0, 99)
        random_value = Decimal('%d.%d' % random_value)
        yield random_date, random_value


