# Generated by Django 5.1.2 on 2024-12-11 10:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("head", "0003_customer_form_page_alter_head_admin_id_lead_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="head",
            name="admin_id",
            field=models.CharField(
                blank=True, default="063e207c", max_length=8, unique=True
            ),
        ),
    ]