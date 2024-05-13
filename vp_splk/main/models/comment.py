from django.db import models
from django.urls import reverse

from main.models.supply import Supply
from main.models.supply_chain import SupplyChain


class Comment(models.Model):
    comment_text = models.CharField(max_length=500, null=False, verbose_name='Комментарий')
    supply = models.ForeignKey(Supply, on_delete=models.CASCADE, verbose_name='Доставка')
    supply_chain = models.ForeignKey(SupplyChain, on_delete=models.CASCADE, verbose_name='Цепь доставки', null=True)
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_text

    class Meta:
        ordering = ['supply', 'supply_chain', '-time_create']
        indexes = [
            models.Index(fields=['supply', 'supply_chain', '-time_create'])
        ]

    #
    # def get_absolute_url(self):
    #     return reverse('cargo', kwargs={'supply_id': self.supply_id, 'cargo_id': self.id})