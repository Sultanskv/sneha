# Generated by Django 5.0.4 on 2024-12-10 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0002_alter_employeedt_employee_admin_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeedt',
            name='Employee_id',
            field=models.CharField(blank=True, default='9b5eb731', max_length=8, unique=True),
        ),
    ]
