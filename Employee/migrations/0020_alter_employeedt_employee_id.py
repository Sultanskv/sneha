# Generated by Django 5.1.2 on 2024-12-13 11:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Employee", "0019_alter_employeedt_employee_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employeedt",
            name="Employee_id",
            field=models.CharField(
                blank=True, default="ccf4af5b", max_length=8, unique=True
            ),
        ),
    ]
