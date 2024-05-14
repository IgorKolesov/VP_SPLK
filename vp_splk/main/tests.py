from django.test import SimpleTestCase
from django.urls import resolve
from .views import (
    Index, notifications, Supplies, ShowSupply, ShowCargo, ShowSupplyChain,
    AddSupply, AddCargo, AddSupplyChain, UpdateSupply, UpdateCargo, UpdateSupplyChain
)

from django.test import TestCase
from django.utils import timezone

from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Cargo, Comment, DeliveryType, Status, Supply, SupplyChain, UploadFiles
from users.models import Company

from main.forms import AddNewSupply, AddNewCargo, AddNewSupplyChain, UploadFileForm, CommentForm

User = get_user_model()


class CargoModelTest(TestCase):

    def setUp(self):
        self.supply = Supply.objects.create(name="Test Supply")
        self.cargo = Cargo.objects.create(
            name="Test Cargo",
            supply=self.supply,
            description="Test Description",
            type="Test Type",
            weight=10.0,
            length=1.0,
            width=1.0,
            height=1.0,
            amount=5,
            units=Cargo.Units.kilo
        )

    def test_cargo_creation(self):
        self.assertEqual(self.cargo.name, "Test Cargo")
        self.assertEqual(self.cargo.supply, self.supply)
        self.assertEqual(self.cargo.description, "Test Description")
        self.assertEqual(self.cargo.type, "Test Type")
        self.assertEqual(self.cargo.weight, 10.0)
        self.assertEqual(self.cargo.length, 1.0)
        self.assertEqual(self.cargo.width, 1.0)
        self.assertEqual(self.cargo.height, 1.0)
        self.assertEqual(self.cargo.amount, 5)
        self.assertEqual(self.cargo.units, Cargo.Units.kilo)

    def test_cargo_absolute_url(self):
        self.assertEqual(self.cargo.get_absolute_url(), f"/main/supplies/{self.supply.id}/cargo/{self.cargo.id}/")


class CommentModelTest(TestCase):

    def setUp(self):
        self.supply = Supply.objects.create(name="Test Supply")
        self.comment = Comment.objects.create(
            comment_text="Test Comment",
            supply=self.supply
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.comment_text, "Test Comment")
        self.assertEqual(self.comment.supply, self.supply)


class DeliveryTypeModelTest(TestCase):

    def setUp(self):
        self.delivery_type = DeliveryType.objects.create(
            name="Test Delivery",
            description="Test Description"
        )

    def test_delivery_type_creation(self):
        self.assertEqual(self.delivery_type.name, "Test Delivery")
        self.assertEqual(self.delivery_type.description, "Test Description")


class StatusModelTest(TestCase):

    def setUp(self):
        self.status = Status.objects.create(
            name="Test Status",
            description="Test Description",
            color="blue"
        )

    def test_status_creation(self):
        self.assertEqual(self.status.name, "Test Status")
        self.assertEqual(self.status.description, "Test Description")
        self.assertEqual(self.status.color, "blue")


class SupplyModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpass')
        self.supply = Supply.objects.create(
            name="Test Supply",
            employee=self.user,
            client=self.user,
            start_point_address="Start Address",
            end_point_address="End Address",
            is_active=Supply.SupplyStatus.ACTIVE,
            deadline=timezone.now()
        )

    def test_supply_creation(self):
        self.assertEqual(self.supply.name, "Test Supply")
        self.assertEqual(self.supply.employee, self.user)
        self.assertEqual(self.supply.client, self.user)
        self.assertEqual(self.supply.start_point_address, "Start Address")
        self.assertEqual(self.supply.end_point_address, "End Address")
        self.assertEqual(self.supply.is_active, Supply.SupplyStatus.ACTIVE)

    def test_supply_absolute_url(self):
        self.assertEqual(self.supply.get_absolute_url(), f"/main/supplies/{self.supply.id}/")


class SupplyChainModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpass')
        self.company = Company.objects.create(name="Test Company")
        self.supply = Supply.objects.create(
            name="Test Supply",
            employee=self.user,
            client=self.user,
            start_point_address="Start Address",
            end_point_address="End Address",
            is_active=Supply.SupplyStatus.ACTIVE,
            deadline=timezone.now()
        )
        self.status = Status.objects.create(name="In Progress", description="In Progress Status")
        self.delivery_type = DeliveryType.objects.create(name="Ground", description="Ground Delivery")
        self.supply_chain = SupplyChain.objects.create(
            name="Test Supply Chain",
            supply=self.supply,
            status=self.status,
            delivery_type=self.delivery_type,
            serial_number=1,
            contractor=self.company,
            start_point_address="Chain Start",
            end_point_address="Chain End",
            deadline=timezone.now()
        )

    def test_supply_chain_creation(self):
        self.assertEqual(self.supply_chain.name, "Test Supply Chain")
        self.assertEqual(self.supply_chain.supply, self.supply)
        self.assertEqual(self.supply_chain.status, self.status)
        self.assertEqual(self.supply_chain.delivery_type, self.delivery_type)
        self.assertEqual(self.supply_chain.serial_number, 1)
        self.assertEqual(self.supply_chain.contractor, self.company)
        self.assertEqual(self.supply_chain.start_point_address, "Chain Start")
        self.assertEqual(self.supply_chain.end_point_address, "Chain End")

    def test_supply_chain_absolute_url(self):
        self.assertEqual(self.supply_chain.get_absolute_url(), f"/main/supplies/{self.supply.id}/chain/{self.supply_chain.id}/")


class UploadFilesModelTest(TestCase):

    def setUp(self):
        self.supply = Supply.objects.create(name="Test Supply")
        self.supply_chain = SupplyChain.objects.create(
            name="Test Supply Chain",
            supply=self.supply,
            status=Status.objects.create(name="In Progress", description="In Progress Status"),
            delivery_type=DeliveryType.objects.create(name="Ground", description="Ground Delivery"),
            serial_number=1,
            start_point_address="Chain Start",
            end_point_address="Chain End",
            deadline=timezone.now()
        )
        self.upload_file = UploadFiles.objects.create(
            file="test_file.txt",
            supply=self.supply,
            supply_chain=self.supply_chain
        )

    def test_upload_file_creation(self):
        self.assertEqual(self.upload_file.file, "test_file.txt")
        self.assertEqual(self.upload_file.supply, self.supply)
        self.assertEqual(self.upload_file.supply_chain, self.supply_chain)



class TestClientViews(TestCase):
    def setUp(self):
        # Создание тестового пользователя-клиента
        self.client_user = get_user_model().objects.create_user(
            username='clientuser', password='clientpass')

        # Создание тестовой поставки для клиента
        self.supply = Supply.objects.create(name="Test Supply", client=self.client_user)

    def test_index_view_for_client(self):
        # Тестирование доступа к главной странице для клиента
        self.client.login(username='clientuser', password='clientpass')
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/index_page.html')

    def test_show_supply_view_for_client(self):
        # Тестирование просмотра поставки для клиента
        self.client.login(username='clientuser', password='clientpass')
        response = self.client.get(reverse('supply', kwargs={'supply_id': self.supply.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/supply_page.html')

    def test_add_supply_view_for_employee(self):
        # Тестирование доступа к представлению добавления новой доставки для сотрудника
        self.client.login(username='clientuser', password='clientpass')
        response = self.client.get(reverse('add_supply'))
        self.assertEqual(response.status_code, 403)


class TestEmployeeViews(TestCase):
    def setUp(self):
        # Создание тестового пользователя-сотрудника
        self.employee_user = get_user_model().objects.create_user(
            username='employeeuser', password='employeepass')

        # Создание тестовой компании для сотрудника
        self.company = Company.objects.create(name="Test Company")

        # Ассоциирование тестового пользователя-сотрудника с компанией
        self.employee_user.company = self.company
        self.employee_user.save()

    def test_index_view_for_employee(self):
        # Тестирование доступа к главной странице для сотрудника
        self.client.login(username='employeeuser', password='employeepass')
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/index_page.html')

    def test_add_supply_view_for_employee(self):
        # Тестирование доступа к представлению добавления новой доставки для сотрудника
        self.client.login(username='employeeuser', password='employeepass')
        response = self.client.get(reverse('add_supply'))
        self.assertEqual(response.status_code, 403)


class TestValidForms(TestCase):
    def test_valid_add_new_supply_form(self):
        client = get_user_model().objects.create_user(username='employeeuser', password='employeepass')
        form_data = {
            'name': 'Test Supply',
            'start_point_address': 'Start Address',
            'end_point_address': 'End Address',
            'employee': 0,
            'client': client,
            'deadline': timezone.now(),
        }
        form = AddNewSupply(data=form_data)
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_valid_add_new_cargo_form(self):
        form_data = {
            'name': 'Test Cargo',
            'description': 'Test Description',
            'supply': 10,
            'type': 'test_type',
            'units': 'шт',
            'weight': 0.5,
            'length': 0.2,
            'width': 10.0,
            'height': 1000.0,
            'amount': 5,
        }
        form = AddNewCargo(data=form_data)
        self.assertTrue(form.is_valid())

    def test_valid_add_new_supply_chain_form(self):
        status = Status.objects.create(name='test')
        delivery_type = DeliveryType.objects.create(name='test')
        company = Company.objects.create(name='test')

        form_data = {
            'name': 'Test Supply Chain',
            'start_point_address': 'Start Address',
            'end_point_address': 'End Address',
            'status': status,
            'delivery_type': delivery_type,
            'contractor': company,
            'deadline': timezone.now(),
        }
        form = AddNewSupplyChain(data=form_data)
        self.assertTrue(form.is_valid())

    def test_valid_comment_form(self):
        form_data = {
            'comment_text': 'Test Comment',
        }
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())


class TestInvalidForms(TestCase):
    def test_invalid_add_new_supply_form(self):
        form_data = {
            'name': '',
            'start_point_address': 'Start Address',
            'end_point_address': 'End Address',
            'deadline': timezone.now(),
        }
        form = AddNewSupply(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_add_new_cargo_form(self):
        form_data = {
            'name': 'Test Cargo',
            'description': 'Test Description',
            'type': 'asfasdf',
            'weight': '234bwe',
            'length': 0.2,
            'width': 10,
            'height': 1000,
            'amount': 5,
            'units': 'asdf'
        }
        form = AddNewCargo(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_add_new_supply_chain_form(self):
        form_data = {
            'name': 'Test Supply Chain',
            'start_point_address': 'Start Address',
            'end_point_address': None,
            'deadline': timezone.now(),
        }
        form = AddNewSupplyChain(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_upload_file_form(self):
        form_data = {
            'file': None
        }
        form = UploadFileForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_comment_form(self):
        form_data = {
            'comment': None
        }
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())


class TestUrls(SimpleTestCase):

    def test_index_url_resolves(self):
        url = reverse('main')
        self.assertEqual(resolve(url).func.view_class, Index)

    def test_notifications_url_resolves(self):
        url = reverse('notifications')
        self.assertEqual(resolve(url).func, notifications)

    def test_supplies_url_resolves(self):
        url = reverse('supplies')
        self.assertEqual(resolve(url).func.view_class, Supplies)

    def test_show_supply_url_resolves(self):
        url = reverse('supply', args=[1])
        self.assertEqual(resolve(url).func.view_class, ShowSupply)

    def test_show_cargo_url_resolves(self):
        url = reverse('cargo', args=[1, 1])
        self.assertEqual(resolve(url).func.view_class, ShowCargo)

    def test_show_supply_chain_url_resolves(self):
        url = reverse('supply_chain', args=[1, 1])
        self.assertEqual(resolve(url).func.view_class, ShowSupplyChain)

    def test_add_supply_url_resolves(self):
        url = reverse('add_supply')
        self.assertEqual(resolve(url).func.view_class, AddSupply)

    def test_add_cargo_url_resolves(self):
        url = reverse('add_cargo', args=[1])
        self.assertEqual(resolve(url).func.view_class, AddCargo)

    def test_add_supply_chain_url_resolves(self):
        url = reverse('add_supply_chain', args=[1])
        self.assertEqual(resolve(url).func.view_class, AddSupplyChain)

    def test_edit_supply_url_resolves(self):
        url = reverse('edit_supply', args=[1])
        self.assertEqual(resolve(url).func.view_class, UpdateSupply)

    def test_edit_cargo_url_resolves(self):
        url = reverse('edit_cargo', args=[1, 1])
        self.assertEqual(resolve(url).func.view_class, UpdateCargo)

    def test_edit_chain_url_resolves(self):
        url = reverse('edit_chain', args=[1, 1])
        self.assertEqual(resolve(url).func.view_class, UpdateSupplyChain)
