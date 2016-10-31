from django.shortcuts import render
from datetime import date
from decimal import Decimal
from .models import Account, Charge
from random import randint
from .models import Account
# Create your views here.


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


def main(request):
    return render(request, 'finance/charges_page.html')


def charges(request):
    charges = []
    positive = 0
    negative = 0
    for i in range(25):
        Date, Value = random_transactions().__next__()
        if Value > 0 : positive+= Value
        else : negative+= Value
        charge = Charge.create(Value, Date)
        charges.append(charge)

    return render(request,
                  'finance/charges_view.html',
                  {"charges": charges, "positive" : positive, "negative" : negative})
