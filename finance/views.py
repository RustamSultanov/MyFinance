from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def front_page(request):
	return HttpResponse('<html>'
                        '<head>'
                        '<title>Главная страница</title>'
                        '</head>'
                        '<body>'
                        '<h1>Приветствие</h1><br>'
                        '<a href="charges">Выписка по счету</a>'
                        '<body/>'
                        '</html>')

def charges_page(request):
	return HttpResponse('<html>'
                        '<head>'
                        '<title>Выписка по счету</title>'
                        '</head>'
                        '<body>'
                        '<h1>Выписка по счету</h1><br>'
                        '<table border=3>'
                        '<tr>'
                        '<td>'
                        'Один'
                        '</td>'
                        '<td>'
                        'Четыре'
                        '</td>'
                        '</tr>'
                        '<tr>'
                        '<td>'
                        'Два'
                        '</td>'
                        '<td>'
                        'Пять'
                        '</td>'
                        '</tr>'
                        '<tr>'
                        '<td>'
                        'Три'
                        '</td>'
                        '<td>'
                        'Шесть'
                        '</td>'
                        '</tr>'
                        '</table>'
                        '<a href="/">Главная страница</a>'
                        '<body/>'
                        '</html>')