# Generated by Django 4.2.1 on 2024-05-14 16:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0007_comment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="supply",
            name="deadline",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="Крайний срок"
            ),
        ),
    ]