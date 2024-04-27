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
        ACTIVE = 1, 'Действующая доставка'
        NON_ACTIVE = 0, 'Выполненная доставка'

    name = models.CharField(max_length=100)
    # employee_id =
    # client_id =
    start_point_address = models.CharField(max_length=250)
    end_point_address = models.CharField(max_length=250)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(choices=Status.choices, default=Status.ACTIVE)

    objects = models.Manager()
    active = ActiveSuppliesManager()
    non_active = NonActiveSuppliesManager()

    def __str__(self):
        return self.name

    class Meta:
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

