from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView

from .models import Supply, Cargo, SupplyChain, UploadFiles
from .forms import AddNewSupply, AddNewCargo, AddNewSupplyChain, UploadFileForm
from .utils import DataMixin

menu = [
    {'id': 0, 'title': 'Главная', 'url_name': 'main', 'icon': 'fa-home'},
    {'id': 1, 'title': 'Личный кабинет', 'url_name': 'profile', 'icon': 'fa-user'},
    {'id': 2, 'title': 'Новая доставка', 'url_name': 'add_supply', 'icon': 'fa-truck'},
    {'id': 3, 'title': 'Доставки', 'url_name': 'supplies', 'icon': 'fa-box-open'},
    {'id': 4, 'title': 'Уведомления', 'url_name': 'notifications', 'icon': 'fa-bell'},
]


# def index(request):
#     data = {'title': 'main page'}
#     return render(request, 'main/index_page.html', data)


class Index(DataMixin, TemplateView):
    template_name = 'main/index_page.html'
    title = 'Главная страница'


class Supplies(DataMixin, ListView):
    template_name = 'main/supplies_page.html'
    title = 'Доставки'
    context_object_name = 'supplies'
    paginate_by = 6

    def get_queryset(self):
        return Supply.active.all()


class ShowSupply(DataMixin, DetailView):
    template_name = 'main/supply_page.html'
    pk_url_kwarg = 'supply_id'
    context_object_name = 'supply'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return self.get_mixin_context(context, title=context['supply'].name)

    def get_object(self, queryset=None):
        supply_id = self.kwargs.get('supply_id')
        return get_object_or_404(Supply, pk=supply_id)


class ShowCargo(DataMixin, DetailView):
    template_name = 'main/cargo_page.html'
    pk_url_kwarg = 'cargo_id'
    context_object_name = 'cargo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['cargo'].name)

    def get_object(self, queryset=None):
        supply_id = self.kwargs.get('supply_id')
        cargo_id = self.kwargs.get('cargo_id')
        return get_object_or_404(Cargo, pk=cargo_id, supply_id=supply_id)


class ShowSupplyChain(DataMixin, DetailView):
    template_name = 'main/supply_chain_page.html'
    pk_url_kwarg = 'supply_chain_id'
    context_object_name = 'chain'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['chain'].name)

    def get_object(self, queryset=None):
        supply_id = self.kwargs.get('supply_id')
        supply_chain_id = self.kwargs.get('supply_chain_id')
        return get_object_or_404(SupplyChain, pk=supply_chain_id, supply_id=supply_id)


def profile(request):
    return HttpResponse('profile')


class AddSupply(DataMixin, CreateView):
    form_class = AddNewSupply
    template_name = 'main/forms_pages/add_supply.html'
    title = 'Новая доставка'


class AddCargo(DataMixin, CreateView):
    form_class = AddNewCargo
    template_name = 'main/forms_pages/add_cargo.html'
    title = 'Новый груз'


class AddSupplyChain(DataMixin, CreateView):
    form_class = AddNewSupplyChain
    template_name = 'main/forms_pages/add_supply_chain.html'
    title = 'Добавить цепочку'


class UpdateSupply(DataMixin, UpdateView):
    model = Supply
    fields = '__all__'
    template_name = 'main/forms_pages/add_supply.html'
    title = 'Редактирование доставки'


class UpdateCargo(DataMixin, UpdateView):
    model = Cargo
    fields = '__all__'
    template_name = 'main/forms_pages/add_cargo.html'
    title = 'Редактирование груза'


class UpdateSupplyChain(DataMixin, UpdateView):
    model = SupplyChain
    fields = '__all__'
    template_name = 'main/forms_pages/add_supply_chain.html'
    title = 'Редактирование этапа доставки'


def notifications(request):
    return HttpResponse('notifications')
