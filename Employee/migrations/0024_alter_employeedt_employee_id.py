# Generated by Django 5.1.2 on 2024-12-17 06:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Employee", "0023_alter_employeedt_employee_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employeedt",
            name="Employee_id",
            field=models.CharField(
                blank=True, default="4b58d3d2", max_length=8, unique=True
            ),
        ),
    ]
