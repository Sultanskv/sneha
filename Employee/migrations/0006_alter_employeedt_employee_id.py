# Generated by Django 5.1.2 on 2024-12-11 05:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Employee", "0005_alter_employeedt_employee_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employeedt",
            name="Employee_id",
            field=models.CharField(
                blank=True, default="9dadf811", max_length=8, unique=True
            ),
        ),
    ]