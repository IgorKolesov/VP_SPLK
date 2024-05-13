from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from main.models.delivery_type import DeliveryType
from main.models.status import Status
from main.models.supply import Supply
from users.models import Company


class SupplyChain(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    supply = models.ForeignKey(Supply, on_delete=models.CASCADE, verbose_name='Доставка')
    status = models.ForeignKey(Status, on_delete=models.SET_DEFAULT, default=1, verbose_name='Статус доставки')
    delivery_type = models.ForeignKey(DeliveryType, on_delete=models.SET_DEFAULT, default=1, verbose_name='Тип доставки')
    serial_number = models.IntegerField(default=1, verbose_name='Номер по порядку')
    contractor = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, default=None, verbose_name='Исполнитель')
    start_point_address = models.CharField(max_length=250, verbose_name='Откуда')
    end_point_address = models.CharField(max_length=250, verbose_name='Куда')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время последнего изменения')
    deadline = models.DateTimeField(verbose_name='Крайний срок')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Этапы доставки'
        verbose_name_plural = 'Этапы доставки'

        ordering = ['supply_id', 'serial_number']


    def get_absolute_url(self):
        return reverse('supply_chain', kwargs={'supply_id': self.supply_id, 'supply_chain_id': self.id})


