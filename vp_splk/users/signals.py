from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User


@receiver(post_save, sender=User)
def add_user_to_group(sender, instance, created, **kwargs):
    if created:
        if instance.company:
            group, _ = Group.objects.get_or_create(name='logistic_companies_users')
            instance.groups.add(group)
        else:
            group, _ = Group.objects.get_or_create(name='clients')
            instance.groups.add(group)
