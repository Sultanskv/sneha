# Generated by Django 5.1.2 on 2024-12-18 06:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("head", "0020_alter_head_admin_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="head",
            name="admin_id",
            field=models.CharField(
                blank=True, default="36846409", max_length=8, unique=True
            ),
        ),
    ]
