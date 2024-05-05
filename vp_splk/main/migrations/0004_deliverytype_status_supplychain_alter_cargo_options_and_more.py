# Generated by Django 4.2.1 on 2024-05-02 16:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0003_rename_supply_id_cargo_supply"),
    ]

    operations = [
        migrations.CreateModel(
            name="DeliveryType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=30, verbose_name="Название")),
                (
                    "description",
                    models.CharField(max_length=300, verbose_name="Описание"),
                ),
                (
                    "time_create",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Время создания"
                    ),
                ),
                (
                    "time_update",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Время последнего изменения"
                    ),
                ),
            ],
            options={
                "verbose_name": "Тип доставки",
                "verbose_name_plural": "Типы доставки",
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="Status",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=30, verbose_name="Название")),
                (
                    "description",
                    models.CharField(max_length=300, verbose_name="Описание"),
                ),
                (
                    "time_create",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Время создания"
                    ),
                ),
                (
                    "time_update",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Время последнего изменения"
                    ),
                ),
            ],
            options={
                "verbose_name": "Статус доставки",
                "verbose_name_plural": "Статусы доставки",
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="SupplyChain",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="Название")),
                (
                    "serial_number",
                    models.IntegerField(default=1, verbose_name="Номер по порядку"),
                ),
                (
                    "start_point_address",
                    models.CharField(max_length=250, verbose_name="Откуда"),
                ),
                (
                    "end_point_address",
                    models.CharField(max_length=250, verbose_name="Куда"),
                ),
                (
                    "time_create",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Время создания"
                    ),
                ),
                (
                    "time_update",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Время последнего изменения"
                    ),
                ),
                ("deadline", models.DateTimeField(verbose_name="Крайний срок")),
            ],
            options={
                "verbose_name": "Этапы доставки",
                "verbose_name_plural": "Этапы доставки",
                "ordering": ["-time_create", "serial_number"],
            },
        ),
        migrations.AlterModelOptions(
            name="cargo",
            options={"ordering": ["supply", "-time_create"]},
        ),
        migrations.AlterModelOptions(
            name="supply",
            options={
                "ordering": ["-time_create"],
                "verbose_name": "Доставки",
                "verbose_name_plural": "Доставки",
            },
        ),
        migrations.AlterField(
            model_name="cargo",
            name="amount",
            field=models.IntegerField(default=1, verbose_name="Количество"),
        ),
        migrations.AlterField(
            model_name="cargo",
            name="description",
            field=models.CharField(max_length=500, verbose_name="Описание груза"),
        ),
        migrations.AlterField(
            model_name="cargo",
            name="height",
            field=models.FloatField(default=0, verbose_name="Высота"),
        ),
        migrations.AlterField(
            model_name="cargo",
            name="length",
            field=models.FloatField(default=0, verbose_name="Длина"),
        ),
        migrations.AlterField(
            model_name="cargo",
            name="name",
            field=models.CharField(max_length=250, verbose_name="Название"),
        ),
        migrations.AlterField(
            model_name="cargo",
            name="supply",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="main.supply",
                verbose_name="Доставка",
            ),
        ),
        migrations.AlterField(
            model_name="cargo",
            name="type",
            field=models.CharField(max_length=250, verbose_name="Тип груза"),
        ),
        migrations.AlterField(
            model_name="cargo",
            name="units",
            field=models.CharField(
                choices=[("кг", "килограммы"), ("шт", "штуки"), ("л", "литры")],
                default="шт",
                verbose_name="Единицы измерения",
            ),
        ),
        migrations.AlterField(
            model_name="cargo",
            name="weight",
            field=models.FloatField(default=0, verbose_name="Вес"),
        ),
        migrations.AlterField(
            model_name="cargo",
            name="width",
            field=models.FloatField(default=0, verbose_name="Ширина"),
        ),
        migrations.AlterField(
            model_name="supply",
            name="end_point_address",
            field=models.CharField(max_length=250, verbose_name="Куда"),
        ),
        migrations.AlterField(
            model_name="supply",
            name="is_active",
            field=models.BooleanField(
                choices=[(1, "В работе"), (0, "Завершена")],
                default=1,
                verbose_name="Статус доставки",
            ),
        ),
        migrations.AlterField(
            model_name="supply",
            name="name",
            field=models.CharField(max_length=100, verbose_name="Название"),
        ),
        migrations.AlterField(
            model_name="supply",
            name="start_point_address",
            field=models.CharField(max_length=250, verbose_name="Откуда"),
        ),
        migrations.AlterField(
            model_name="supply",
            name="time_create",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="Время создания"
            ),
        ),
        migrations.AlterField(
            model_name="supply",
            name="time_update",
            field=models.DateTimeField(
                auto_now=True, verbose_name="Время последнего изменения"
            ),
        ),
        migrations.AddIndex(
            model_name="cargo",
            index=models.Index(
                fields=["supply", "-time_create"], name="main_cargo_supply__23ccee_idx"
            ),
        ),
        migrations.AddField(
            model_name="supplychain",
            name="delivery_type",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                to="main.deliverytype",
                verbose_name="Тип доставки",
            ),
        ),
        migrations.AddField(
            model_name="supplychain",
            name="status",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                to="main.status",
                verbose_name="Статус доставки",
            ),
        ),
        migrations.AddField(
            model_name="supplychain",
            name="supply",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="main.supply",
                verbose_name="Доставка",
            ),
        ),
        migrations.AddIndex(
            model_name="status",
            index=models.Index(fields=["id"], name="main_status_id_035bcf_idx"),
        ),
        migrations.AddIndex(
            model_name="deliverytype",
            index=models.Index(fields=["id"], name="main_delive_id_55ba5e_idx"),
        ),
        migrations.AddIndex(
            model_name="supplychain",
            index=models.Index(
                fields=["-time_create"], name="main_supply_time_cr_67e161_idx"
            ),
        ),
    ]