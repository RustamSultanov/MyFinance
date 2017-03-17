import requests
from django import template
from django.shortcuts import reverse
from decimal import Decimal
from functools import reduce

register = template.Library()


@register.inclusion_tag('account_list.html')
def show_accounts(request):
    headers = {'Authorization': 'JWT ' + request.session["token"]}
    response = requests.get("http://localhost:8000/api/accounts/", headers=headers)
    accounts = response.json()
    for elem in accounts:
        get_charges = requests.get(
            "http://localhost:8000" + reverse("api:charge_list") + "?search=" + elem["number"],
            headers=headers
        )
        account_charges = get_charges.json()
        if len(account_charges) == 0:
            elem["total"] = None
        else:
            elem["total"] = reduce(
                lambda x, y: Decimal(x) + Decimal(y),
                map(lambda x: x["value"], account_charges),
                0.00
            )
    return {'accounts': accounts}
