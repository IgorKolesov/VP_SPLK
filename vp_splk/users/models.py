from django.contrib.auth.models import AbstractUser
from django.db import models


class Company(models.Model):
    class CompanyType(models.TextChoices):
        IP = 'Индивидуальный предприниматель', 'ИП'
        OOO = 'общество с ограниченной ответственностью', 'ООО'
        AO = 'непубличное акционерное общество', 'НАО'
        PAO = 'публичное акционерное общество', 'ПАО'
        KT = 'коммерческое товарищество', 'КТ'
        PK = 'производственный кооператив', 'ПК'
        UP = 'унитарное предприятие', 'УП'
        HT = 'хозяйственное товарищество', 'ХТ'
        HP = 'хозяйственное партнерство', 'ХП'
        NKM = 'некоммерческое юридическое лицо', 'НКО'

    inn = models.CharField(max_length=12, blank=False, null=False, verbose_name='ИНН')
    name = models.CharField(max_length=300, blank=False, null=False, verbose_name='Название')
    bank_account = models.CharField(max_length=20, blank=False, null=False, verbose_name='Расчетный счет')
    company_type = models.CharField(choices=CompanyType.choices, default=CompanyType.IP, verbose_name='Тип компании')
    address = models.CharField(max_length=300, verbose_name='Адрес')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время последнего изменения')

    def __str__(self):
        return  str(self.name) + f' (ИНН: {self.inn})'

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]


class User(AbstractUser):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, verbose_name='Компания')
    phone_number = models.CharField(max_length=15, verbose_name='Номер телефона')
