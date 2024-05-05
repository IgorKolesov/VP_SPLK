from django.db import models
from django.urls import reverse

from main.models.supply import Supply
from main.models.supply_chain import SupplyChain


class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')
    supply = models.ForeignKey(Supply, on_delete=models.CASCADE, verbose_name='Доставка')
    supply_chain = models.ForeignKey(SupplyChain, on_delete=models.CASCADE, verbose_name='Цепь доставки', null=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file.name

    class Meta:
        ordering = ['supply', '-time_create']
        indexes = [
            models.Index(fields=['supply', '-time_create'])
        ]
    #
    # def get_absolute_url(self):
    #     return reverse('cargo', kwargs={'supply_id': self.supply_id, 'cargo_id': self.id})