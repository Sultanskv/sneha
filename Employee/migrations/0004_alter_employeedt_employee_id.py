# Generated by Django 5.1.2 on 2024-12-10 07:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Employee", "0003_alter_employeedt_employee_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employeedt",
            name="Employee_id",
            field=models.CharField(
                blank=True, default="383b783f", max_length=8, unique=True
            ),
        ),
    ]