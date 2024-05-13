from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.views import LoginView

from users.models import Company


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form_input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form_input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form_input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form_input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form_input'}))
    company = forms.ModelChoiceField(queryset=Company.objects.all(), required=False, label='Компания (оставьте пустым, если вы клиент)')

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'company', 'password1', 'password2']
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }

        widgets = {
            'email': forms.TextInput(attrs={'class': 'form_input'}),
            'first_name': forms.TextInput(attrs={'class': 'form_input'}),
            'last_name': forms.TextInput(attrs={'class': 'form_input'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким e-mail уже существует')

        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']

        if not phone_number.startswith('+7') and not phone_number.startswith('8'):
            raise forms.ValidationError('Номер телефона должен начинаться с +7 или 8')

        if (((phone_number.startswith('+7')) and (len(phone_number[1:]) != 10)) or
                ((phone_number.startswith('8')) and (len(phone_number[1:]) != 10))):
            raise forms.ValidationError('Слишком короткий номер телефона')

        if phone_number.startswith('8'):
            return '+7' + phone_number[1:]

        return phone_number


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Логин', widget=forms.TextInput(attrs={'class': 'form_input'}))
    email = forms.CharField(disabled=True, label='E-mail', widget=forms.TextInput(attrs={'class': 'form_input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'company']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form_input'}),
            'last_name': forms.TextInput(attrs={'class': 'form_input'}),
        }


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput(attrs={'class': 'form_input'}))
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(attrs={'class': 'form_input'}))
    new_password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form_input'}))


class AddNewCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['company_type', 'name', 'inn', 'bank_account', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form_input'}),
        }

    def clean_inn(self):
        inn = self.cleaned_data['inn']
        if Company.objects.filter(inn=inn).exists():
            raise forms.ValidationError('Компания с таким ИНН уже зарегистрирована')
        if (len(inn) != 12) or (not inn.isdigit()):
            raise forms.ValidationError('ИНН должен состоять из 12 цифр')
        return inn

    def clean_bank_account(self):
        bank_account = self.cleaned_data['bank_account']
        if (len(bank_account) != 20) or (not bank_account.isdigit()):
            raise forms.ValidationError('Расчетный счет должен состоять из 20 цифр')
        return bank_account
