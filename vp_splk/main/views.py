from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string

from .models import Supply, Cargo, SupplyChain, UploadFiles
from .forms import AddNewSupply, AddNewCargo, AddNewSupplyChain, UploadFileForm

menu = [
    {'id': 0, 'title': 'Главная', 'url_name': 'main', 'icon': 'fa-home'},
    {'id': 1, 'title': 'Личный кабинет', 'url_name': 'profile', 'icon': 'fa-user'},
    {'id': 2, 'title': 'Новая доставка', 'url_name': 'add_supply', 'icon': 'fa-truck'},
    {'id': 3, 'title': 'Доставки', 'url_name': 'supplies', 'icon': 'fa-box-open'},
    {'id': 4, 'title': 'Уведомления', 'url_name': 'notifications', 'icon': 'fa-bell'},
]


def index(request):
    data = {'title': 'main page'}
    return render(request, 'main/index_page.html', data)


def supplies(request):
    supplies_db = Supply.active.all()

    supplies_data = {
        'title': 'supplies',
        'supplies': supplies_db,
    }
    return render(request, 'main/supplies_page.html', supplies_data)


def supply(request, supply_id):

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'], supply_id=supply_id)
            fp.save()
    else:
        form = UploadFileForm()

    supply_db = get_object_or_404(Supply, pk=supply_id)
    cargo_db = Cargo.objects.filter(supply=supply_id)
    chains_db = SupplyChain.objects.filter(supply=supply_id)

    supply_data = {
        'title': supply_db.name,
        'supply': supply_db,
        'cargos': cargo_db,
        'supply_chains': chains_db,
        'form': form,
    }
    return render(request, 'main/supply_page.html', supply_data)


def cargo(request, supply_id, cargo_id):
    cargo_db = get_object_or_404(Cargo, supply_id=supply_id, pk=cargo_id)

    supply_data = {
        'title': cargo_db.id,
        'cargo': cargo_db,
    }
    return render(request, 'main/cargo_page.html', supply_data)


def supply_chain(request, supply_id, supply_chain_serial_number):
    chains_db = get_object_or_404(SupplyChain, supply_id=supply_id, serial_number=supply_chain_serial_number)

    supply_data = {
        'title': chains_db.name,
        'chain': chains_db,
    }
    return render(request, 'main/supply_chain_page.html', supply_data)


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

    return render(request, 'main/forms_pages/add_supply.html', data)


def add_cargo(request, supply_id):
    if request.method == 'POST':
        form = AddNewCargo(request.POST)
        if form.is_valid():
            added_cargo = form.save(commit=False)
            added_cargo.supply_id = supply_id
            added_cargo.save()
            return redirect('supply', supply_id)
    else:
        form = AddNewCargo()

    data = {
        'title': 'Добавить груз',
        'form': form,
    }

    return render(request, 'main/forms_pages/add_cargo.html', data)


def add_supply_chain(request, supply_id):
    if request.method == 'POST':
        form = AddNewSupplyChain(request.POST)
        if form.is_valid():
            added_chain = form.save(commit=False)
            added_chain.supply_id = supply_id
            added_chain.save()
            return redirect('supply', supply_id)
    else:
        form = AddNewSupplyChain()

    data = {
        'title': 'Добавить цепочку',
        'form': form,
    }

    return render(request, 'main/forms_pages/add_supply_chain.html', data)

def notifications(request):
    return HttpResponse('notifications')
