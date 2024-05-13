from datetime import date

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class ActiveSuppliesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=Supply.SupplyStatus.ACTIVE)


class NonActiveSuppliesManager(models.Manager):
    def get_queryset(self):
        return super().get_quertset().filter(is_active=Supply.SupplyStatus.NON_ACTIVE)


class Supply(models.Model):
    class SupplyStatus(models.IntegerChoices):
        ACTIVE = 1, 'В работе'
        NON_ACTIVE = 0, 'Завершена'

    name = models.CharField(max_length=100, verbose_name='Название')
    employee = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, default=None, verbose_name='Ответственный', related_name='supplies_as_employee')
    client = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, default=None, verbose_name='Клиент', related_name='supplies_as_client')
    start_point_address = models.CharField(max_length=250, verbose_name='Откуда')
    end_point_address = models.CharField(max_length=250, verbose_name='Куда')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время последнего изменения')
    is_active = models.BooleanField(choices=SupplyStatus.choices, default=SupplyStatus.ACTIVE, verbose_name='Статус доставки')
    deadline = models.DateTimeField(verbose_name='Крайний срок', default=date.today(), null=False)

    objects = models.Manager()
    active = ActiveSuppliesManager()
    non_active = NonActiveSuppliesManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Доставки'
        verbose_name_plural = 'Доставки'

        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def get_absolute_url(self):
        return reverse('supply', kwargs={'supply_id': self.id})

