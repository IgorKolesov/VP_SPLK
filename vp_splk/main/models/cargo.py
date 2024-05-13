from django.db import models
from django.urls import reverse

from main.models.supply import Supply


class Cargo(models.Model):
    class Units(models.TextChoices):
        kilo = 'кг', 'килограммы'
        unit = 'шт', 'штуки'
        litre = 'л', 'литры'
        pallet = 'паллет', 'паллет'

    name = models.CharField(max_length=250, verbose_name='Название')
    supply = models.ForeignKey(Supply, on_delete=models.CASCADE, verbose_name='Доставка')
    description = models.CharField(max_length=500, verbose_name='Описание груза')
    type = models.CharField(max_length=250, verbose_name='Тип груза')
    weight = models.FloatField(default=0, verbose_name='Вес (кг)')
    length = models.FloatField(default=0, verbose_name='Длина (м)')
    width = models.FloatField(default=0, verbose_name='Ширина (м)')
    height = models.FloatField(default=0, verbose_name='Высота (м)')
    amount = models.IntegerField(default=1, verbose_name='Количество')
    units = models.CharField(choices=Units.choices, default=Units.unit, verbose_name='Единицы измерения')
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