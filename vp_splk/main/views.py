from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string

from .models import Supply, Cargo
from .forms import AddNewSupply, AddNewCargo

menu = [
    {'id': 0, 'title': 'Главная', 'url_name': 'main', 'icon': 'fa-home'},
    {'id': 1, 'title': 'Личный кабинет', 'url_name': 'profile', 'icon': 'fa-user'},
    {'id': 2, 'title': 'Новая доставка', 'url_name': 'add_supply', 'icon': 'fa-truck'},
    {'id': 3, 'title': 'Доставки', 'url_name': 'supplies', 'icon': 'fa-box-open'},
    {'id': 4, 'title': 'Уведомления', 'url_name': 'notifications', 'icon': 'fa-bell'},
]


def index(request):
    data = {'title': 'main page'}
    return render(request, 'main/index.html', data)


def supplies(request):
    supplies_db = Supply.active.all()

    supplies_data = {
        'title': 'supplies',
        'supplies': supplies_db,
    }
    return render(request, 'main/supplies.html', supplies_data)


def supply(request, supply_id):
    supply_db = get_object_or_404(Supply, pk=supply_id)
    cargo_db = Cargo.objects.filter(supply=supply_id)

    supply_data = {
        'title': supply_db.name,
        'supply': supply_db,
        'cargos': cargo_db,
    }
    return render(request, 'main/supply.html', supply_data)


def cargo(request, supply_id, cargo_id):
    cargo_db = get_object_or_404(Cargo, pk=cargo_id)

    supply_data = {
        'title': cargo_db.id,
        'cargo': cargo_db,
    }
    return render(request, 'main/cargo.html', supply_data)


def profile(request):
    return HttpResponse('profile')


def add_supply(request):
    if request.method == 'POST':
        form = AddNewSupply(request.POST)
        if form.is_valid():
            added_supply = form.save()
            return redirect('supply', added_supply.id)
    else:
        form = AddNewSupply()

    data = {
        'title': 'Добавить доставку',
        'form': form,
    }

    return render(request, 'main/add_supply.html', data)


def add_cargo(request, supply_id):
    if request.method == 'POST':
        form = AddNewCargo(request.POST)
        if form.is_valid():
            added_cargo = form.save()
            return redirect('supply', added_cargo.supply_id)
    else:
        form = AddNewSupply()

    data = {
        'title': 'Добавить доставку',
        'form': form,
    }

    return render(request, 'main/add_cargo.html', data)


def notifications(request):
    return HttpResponse('notifications')
