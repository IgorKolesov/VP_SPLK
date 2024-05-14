from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import Company, User

from users.forms import (
    LoginUserForm,
    RegisterUserForm,
    ProfileUserForm,
    UserPasswordChangeForm,
    AddNewCompanyForm
)

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth.views import LogoutView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from users import views


class CompanyModelTest(TestCase):

    def setUp(self):
        self.company = Company.objects.create(
            inn="123456789012",
            name="Test Company",
            bank_account="12345678901234567890",
            company_type=Company.CompanyType.IP,
            address="123 Test St, Test City"
        )

    def test_company_creation(self):
        self.assertEqual(self.company.inn, "123456789012")
        self.assertEqual(self.company.name, "Test Company")
        self.assertEqual(self.company.bank_account, "12345678901234567890")
        self.assertEqual(self.company.company_type, Company.CompanyType.IP)
        self.assertEqual(self.company.address, "123 Test St, Test City")

    def test_company_str(self):
        self.assertEqual(str(self.company), "Test Company (ИНН: 123456789012)")

class UserModelTest(TestCase):

    def setUp(self):
        self.company = Company.objects.create(
            inn="123456789012",
            name="Test Company",
            bank_account="12345678901234567890",
            company_type=Company.CompanyType.IP,
            address="123 Test St, Test City"
        )
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
            company=self.company,
            phone_number="1234567890"
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertTrue(self.user.check_password("testpass123"))
        self.assertEqual(self.user.company, self.company)
        self.assertEqual(self.user.phone_number, "1234567890")


class FormTests(TestCase):

    def setUp(self):
        self.company = Company.objects.create(
            inn="123456789012",
            name="Test Company",
            bank_account="12345678901234567890",
            address="123 Test St, Test City"
        )
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            first_name="Test",
            last_name="User",
            phone_number="+71234567890",
            password="testpass123",
            company=self.company
        )

    def test_login_user_form_valid(self):
        form_data = {'username': 'testuser', 'password': 'testpass123'}
        form = LoginUserForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_register_user_form_valid(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'phone_number': '81234567891',
            'password1': 'newuserpass123',
            'password2': 'newuserpass123',
            'company': self.company.id
        }
        form = RegisterUserForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_register_user_form_invalid_email(self):
        get_user_model().objects.create_user(username="anotheruser", email="duplicate@example.com")
        form_data = {
            'username': 'newuser',
            'email': 'duplicate@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'phone_number': '+71234567891',
            'password1': 'newuserpass123',
            'password2': 'newuserpass123',
            'company': self.company.id
        }
        form = RegisterUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_register_user_form_invalid_phone_number(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'phone_number': '1234567890',
            'password1': 'newuserpass123',
            'password2': 'newuserpass123',
            'company': self.company.id
        }
        form = RegisterUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)

    def test_profile_user_form_valid(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '+71234567890',
            'company': self.company.id
        }
        form = ProfileUserForm(instance=self.user, data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_password_change_form_valid(self):
        form_data = {
            'old_password': 'testpass123',
            'new_password1': 'newtestpass123',
            'new_password2': 'newtestpass123'
        }
        form = UserPasswordChangeForm(user=self.user, data=form_data)
        self.assertTrue(form.is_valid())

    def test_add_new_company_form_valid(self):
        form_data = {
            'company_type': Company.CompanyType.OOO,
            'name': 'Another Test Company',
            'inn': '098765432109',
            'bank_account': '09876543210987654321',
            'address': '456 Another Test St, Test City'
        }
        form = AddNewCompanyForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_add_new_company_form_invalid_inn(self):
        form_data = {
            'company_type': Company.CompanyType.OOO,
            'name': 'Another Test Company',
            'inn': '12345',
            'bank_account': '09876543210987654321',
            'address': '456 Another Test St, Test City'
        }
        form = AddNewCompanyForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('inn', form.errors)

    def test_add_new_company_form_invalid_bank_account(self):
        form_data = {
            'company_type': Company.CompanyType.OOO,
            'name': 'Another Test Company',
            'inn': '098765432109',
            'bank_account': '09876',
            'address': '456 Another Test St, Test City'
        }
        form = AddNewCompanyForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('bank_account', form.errors)

    def test_user_password_change_form_invalid(self):
        form_data = {
            'old_password': 'testpass123',
            'new_password1': 'newtestpass123',
            'new_password2': 'newtestpass1234'
        }
        form = UserPasswordChangeForm(user=self.user, data=form_data)
        self.assertFalse(form.is_valid())


class UsersURLTests(SimpleTestCase):

    def test_login_url_resolves(self):
        url = reverse('users:login')
        self.assertEqual(resolve(url).func.view_class, views.LoginUser)

    def test_logout_url_resolves(self):
        url = reverse('users:logout')
        self.assertEqual(resolve(url).func.view_class, LogoutView)

    def test_password_change_url_resolves(self):
        url = reverse('users:password_change')
        self.assertEqual(resolve(url).func.view_class, views.UserPasswordChange)

    def test_password_change_done_url_resolves(self):
        url = reverse('users:password_change_done')
        self.assertEqual(resolve(url).func.view_class, PasswordChangeDoneView)

    def test_password_reset_url_resolves(self):
        url = reverse('users:password_reset')
        self.assertEqual(resolve(url).func.view_class, PasswordResetView)

    def test_password_reset_done_url_resolves(self):
        url = reverse('users:password_reset_done')
        self.assertEqual(resolve(url).func.view_class, PasswordResetDoneView)

    def test_password_reset_confirm_url_resolves(self):
        url = reverse('users:password_reset_confirm', args=['uidb64', 'token'])
        self.assertEqual(resolve(url).func.view_class, PasswordResetConfirmView)

    def test_password_reset_complete_url_resolves(self):
        url = reverse('users:password_reset_complete')
        self.assertEqual(resolve(url).func.view_class, PasswordResetCompleteView)

    def test_register_url_resolves(self):
        url = reverse('users:register')
        self.assertEqual(resolve(url).func.view_class, views.RegisterUsers)

    def test_profile_url_resolves(self):
        url = reverse('users:profile')
        self.assertEqual(resolve(url).func.view_class, views.ProfileUser)

    def test_new_company_url_resolves(self):
        url = reverse('users:new_company')
        self.assertEqual(resolve(url).func.view_class, views.AddNewCompany)


class UsersViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')

    def test_login_view_get(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertIsInstance(response.context['form'], LoginUserForm)
        self.assertContains(response, 'Авторизация')

    def test_login_view_post(self):
        response = self.client.post(reverse('users:login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertRedirects(response, reverse('main'))  # Assuming that after login, user is redirected to 'main'

    def test_register_view_get(self):
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertIsInstance(response.context['form'], RegisterUserForm)
        self.assertContains(response, 'Регистрация')

    def test_register_view_post(self):
        response = self.client.post(reverse('users:register'), {
            'username': 'newuser',
            'first_name': 'test',
            'last_name': 'test',
            'phone_number': "89999999999",
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
            'email': 'newuser@example.com'
        })
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(get_user_model().objects.filter(username='newuser').exists())

    def test_profile_view_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertIsInstance(response.context['form'], ProfileUserForm)
        self.assertContains(response, 'Профиль')

    def test_password_change_view_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('users:password_change'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/password_change_form.html')
        self.assertIsInstance(response.context['form'], UserPasswordChangeForm)
        self.assertContains(response, 'Старый пароль')

    def test_add_new_company_view_get(self):
        response = self.client.get(reverse('users:new_company'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/new_company.html')
        self.assertIsInstance(response.context['form'], AddNewCompanyForm)
        self.assertContains(response, 'Новая компания')

    def test_add_new_company_view_post(self):
        response = self.client.post(reverse('users:new_company'), {
            'company_type': Company.CompanyType.IP,
            'name': 'Test Company',
            'inn': '123456789012',
            'bank_account': '12345678901234567890',
            'address': 'Test Address'
        })
        self.assertRedirects(response, reverse('users:register'))
        self.assertTrue(Company.objects.filter(name='Test Company').exists())
