# Generated by Django 5.1.2 on 2024-12-13 10:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("crm", "0029_alter_super_admin_super_admin_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="lead",
            name="city",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="super_admin",
            name="super_admin_id",
            field=models.CharField(
                blank=True, default="d0ac186f", max_length=8, unique=True
            ),
        ),
    ]