from django.db import models
from django.urls import reverse


class DeliveryType(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название')
    description = models.CharField(max_length=300, verbose_name='Описание')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время последнего изменения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип доставки'
        verbose_name_plural = 'Типы доставки'

        ordering = ['id']
        indexes = [
            models.Index(fields=['id'])
        ]
