from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from main.utils import DataMixin
from users.forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm, AddNewCompanyForm


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}


class RegisterUsers(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {
        'title': 'Регистрация'
    }
    success_url = reverse_lazy('users:login')


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': 'Профиль'}

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change_form.html'


class AddNewCompany(CreateView):
    form_class = AddNewCompanyForm
    template_name = 'users/new_company.html'
    extra_context = {
        'title': 'Новая компания'
    }
    success_url = reverse_lazy('users:register')



