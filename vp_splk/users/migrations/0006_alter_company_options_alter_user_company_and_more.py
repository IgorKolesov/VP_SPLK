# Generated by Django 4.2.1 on 2024-05-12 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0005_user_phone_number"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="company",
            options={
                "ordering": ["-time_create"],
                "verbose_name": "Компания",
                "verbose_name_plural": "Компании",
            },
        ),
        migrations.AlterField(
            model_name="user",
            name="company",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="users.company",
                verbose_name="Компания",
            ),
        ),
        migrations.AddIndex(
            model_name="company",
            index=models.Index(
                fields=["-time_create"], name="users_compa_time_cr_856ce5_idx"
            ),
        ),
    ]
