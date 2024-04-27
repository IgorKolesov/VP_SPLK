from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from .models import Supply

menu = [
    {'title': 'Главная', 'url_name': 'main', 'icon': 'fa-home'},
    {'title': 'Личный кабинет', 'url_name': 'profile', 'icon': 'fa-user'},
    {'title': 'Новая доставка', 'url_name': 'new_supply', 'icon': 'fa-truck'},
    {'title': 'Доставки', 'url_name': 'supplies', 'icon': 'fa-box-open'},
    {'title': 'Уведомления', 'url_name': 'notifications', 'icon': 'fa-bell'},
]


def index(request):
    data = {'title': 'main page',
            'menu': menu,
    }
    return render(request, 'main/index.html', data)


def supplies(request):
    supplies_db = Supply.active.all()

    supplies_data = {
        'title': 'supplies',
        'supplies': supplies_db,
        'menu': menu,
    }
    return render(request, 'main/supplies.html', supplies_data)


def supply(request, supply_id):
    supply_db = get_object_or_404(Supply, pk=supply_id)

    supply_data = {
        'title': supply_db.id,
        'menu': menu,
        'supply': supply_db,
    }
    return render(request, 'main/supply.html', supply_data)


def profile(request):
    return HttpResponse('profile')


def new_supply(request):

    return HttpResponse('new_supply')


def notifications(request):
    return HttpResponse('notifications')
