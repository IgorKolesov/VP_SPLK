from django.db import models
from django.urls import reverse


class Status(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название')
    description = models.CharField(max_length=300, verbose_name='Описание')
    color = models.CharField(max_length=20, default='gray', verbose_name='Цвет для интерфейса')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время последнего изменения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус доставки'
        verbose_name_plural = 'Статусы доставки'

        ordering = ['id']
        indexes = [
            models.Index(fields=['id'])
        ]