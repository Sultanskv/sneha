# Generated by Django 5.1.2 on 2024-12-16 11:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("head", "0014_alter_head_admin_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="lead",
            name="city",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="head",
            name="admin_id",
            field=models.CharField(
                blank=True, default="bde692f4", max_length=8, unique=True
            ),
        ),
    ]
