from django.db import models
from django.urls import reverse


class ActiveSuppliesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=Supply.Status.ACTIVE)


class NonActiveSuppliesManager(models.Manager):
    def get_queryset(self):
        return super().get_quertset().filter(is_active=Supply.Status.NON_ACTIVE)


class Supply(models.Model):
    class Status(models.IntegerChoices):
        ACTIVE = 1, 'В работе'
        NON_ACTIVE = 0, 'Завершена'

    name = models.CharField(max_length=100, verbose_name='Название')
    # employee_id =
    # client_id =
    start_point_address = models.CharField(max_length=250, verbose_name='Откуда')
    end_point_address = models.CharField(max_length=250, verbose_name='Куда')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время последнего изменения')
    is_active = models.BooleanField(choices=Status.choices, default=Status.ACTIVE, verbose_name='Статус доставки')

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


class Cargo(models.Model):
    name = models.CharField(max_length=250)
    supply = models.ForeignKey(Supply, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    type = models.CharField(max_length=250)
    weight = models.FloatField(default=1)
    length = models.FloatField(default=1)
    width = models.FloatField(default=1)
    height = models.FloatField(default=1)
    amount = models.IntegerField(default=1)
    units = models.CharField(max_length=250, default='шт.')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['supply', '-time_create']
        indexes = [
            models.Index(fields=['supply', '-time_create'])
        ]

    def get_absolute_url(self):
        return reverse('cargo', kwargs={'supply_id': self.supply_id, 'cargo_id': self.id})