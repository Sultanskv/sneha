# Generated by Django 5.1.2 on 2024-12-11 12:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Employee", "0012_alter_employeedt_employee_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employeedt",
            name="Employee_id",
            field=models.CharField(
                blank=True, default="2dd5c0d4", max_length=8, unique=True
            ),
        ),
    ]
