# Generated by Django 4.2.1 on 2024-04-27 13:55

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0002_cargo_alter_supply_options_alter_supply_is_active_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="cargo",
            old_name="supply_id",
            new_name="supply",
        ),
    ]