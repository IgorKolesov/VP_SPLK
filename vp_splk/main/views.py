from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView

from .models import Supply, Cargo, SupplyChain, UploadFiles
from .forms import AddNewSupply, AddNewCargo, AddNewSupplyChain, UploadFileForm, CommentForm
from .models.comment import Comment
from .utils import DataMixin

menu = [
    {'id': 0, 'title': 'Главная', 'url_name': 'main', 'icon': 'fa-home'},
    {'id': 1, 'title': 'Новая доставка', 'url_name': 'add_supply', 'icon': 'fa-truck'},
    {'id': 2, 'title': 'Доставки', 'url_name': 'supplies', 'icon': 'fa-box-open'},
    {'id': 3, 'title': 'Уведомления', 'url_name': 'notifications', 'icon': 'fa-bell'},
]


# def index(request):
#     data = {'title': 'main page'}
#     return render(request, 'main/index_page.html', data)


class Index(DataMixin, ListView):
    template_name = 'main/index_page.html'
    title = 'Главная страница'
    context_object_name = 'supplies'

    def get_queryset(self):
        return Supply.objects.all().filter(employee=self.request.user.id).order_by('-time_update')[:3]


class Supplies(DataMixin, ListView):
    template_name = 'main/supplies_page.html'
    title = 'Доставки'
    context_object_name = 'supplies'
    paginate_by = 6

    def get_queryset(self):
        if self.request.user.company is not None:
            return Supply.objects.all().filter(employee=self.request.user.id)
        else:
            return Supply.objects.all().filter(client=self.request.user.id)


class ShowSupply(DataMixin, DetailView):
    template_name = 'main/supply_page.html'
    pk_url_kwarg = 'supply_id'
    context_object_name = 'supply'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.all().filter(supply=self.kwargs.get('supply_id'), supply_chain_id=None)
        print(comments)
        return self.get_mixin_context(context, title=context['supply'].name, file_form=UploadFileForm, supply_chain_comments=comments, comment_form=CommentForm)

    def get_object(self, queryset=None):
        supply_id = self.kwargs.get('supply_id')
        user_id = self.request.user.id
        if self.request.user.company is not None:
            return get_object_or_404(Supply, pk=supply_id, employee=user_id)
        else:
            return get_object_or_404(Supply, pk=supply_id, client=user_id)

    def post(self, request, *args, **kwargs):
        supply_id = self.kwargs.get('supply_id')
        supply = get_object_or_404(Supply, pk=supply_id)

        if 'file' in request.FILES:
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                upload_file = form.save(commit=False)
                upload_file.supply = supply
                upload_file.save()
                return redirect('supply', supply_id=supply_id)
            else:
                return self.render_to_response(self.get_context_data(upload_file_form=form))
        if 'comment_text' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.supply = supply
                comment.save()
                return redirect('supply', supply_id=supply_id)
            else:
                return self.render_to_response(self.get_context_data(comment_form=comment_form))


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
        files = UploadFiles.objects.all().filter(supply_id=self.kwargs.get('supply_id'), supply_chain_id=self.kwargs.get('supply_chain_id'))
        comments = Comment.objects.all().filter(supply_id=self.kwargs.get('supply_id'), supply_chain_id=self.kwargs.get('supply_chain_id'))
        return self.get_mixin_context(context,
                                      title=context['chain'].name,
                                      supply_chain_files=files,
                                      file_form=UploadFileForm,
                                      supply_chain_comments=comments,
                                      comment_form=CommentForm
                                      )

    def get_object(self, queryset=None):
        supply_id = self.kwargs.get('supply_id')
        supply_chain_id = self.kwargs.get('supply_chain_id')
        return get_object_or_404(SupplyChain, pk=supply_chain_id, supply_id=supply_id)

    def post(self, request, *args, **kwargs):

        supply_id = self.kwargs.get('supply_id')
        supply_chain_id = self.kwargs.get('supply_chain_id')

        supply = get_object_or_404(Supply, pk=supply_id)
        supply_chain = get_object_or_404(SupplyChain, supply=supply, pk=supply_chain_id)
        print(request.POST)
        if 'file' in request.FILES:
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                upload_file = form.save(commit=False)
                upload_file.supply = supply
                upload_file.supply_chain = supply_chain
                upload_file.save()
                return redirect('supply_chain', supply_id=supply_id, supply_chain_id=supply_chain_id)
            else:
                return self.render_to_response(self.get_context_data(upload_file_form=form))
        if 'comment_text' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.supply = supply
                comment.supply_chain = supply_chain
                comment.save()
                return redirect('supply_chain', supply_id=supply_id, supply_chain_id=supply_chain_id)
            else:
                return self.render_to_response(self.get_context_data(comment_form=comment_form))


class AddSupply(PermissionRequiredMixin, DataMixin, CreateView):
    form_class = AddNewSupply
    template_name = 'main/forms_pages/add_supply.html'
    title = 'Новая доставка'
    permission_required = 'main.add_supply'

    def form_valid(self, form):
        s = form.save(commit=False)
        s.employee = self.request.user
        return super().form_valid(form)


class AddCargo(PermissionRequiredMixin, DataMixin, CreateView):
    form_class = AddNewCargo
    template_name = 'main/forms_pages/add_cargo.html'
    title = 'Новый груз'
    permission_required = 'main.add_cargo'


class AddSupplyChain(PermissionRequiredMixin, DataMixin, CreateView):
    form_class = AddNewSupplyChain
    template_name = 'main/forms_pages/add_supply_chain.html'
    title = 'Добавить цепочку'
    permission_required = 'main.add_supply_chain'


class UpdateSupply(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Supply
    fields = '__all__'
    template_name = 'main/forms_pages/add_supply.html'
    title = 'Редактирование доставки'
    permission_required = 'main.change_supply'


class UpdateCargo(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Cargo
    fields = '__all__'
    template_name = 'main/forms_pages/add_cargo.html'
    title = 'Редактирование груза'
    permission_required = 'main.change_cargo'


class UpdateSupplyChain(PermissionRequiredMixin, DataMixin, UpdateView):
    model = SupplyChain
    fields = '__all__'
    template_name = 'main/forms_pages/add_supply_chain.html'
    title = 'Редактирование этапа доставки'
    permission_required = 'main.change_supply_chain'


def notifications(request):
    return HttpResponse('notifications')
