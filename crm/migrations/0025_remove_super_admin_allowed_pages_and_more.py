# Generated by Django 5.1.2 on 2024-12-11 11:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("crm", "0024_remove_super_admin_facebook_app_id_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="super_admin",
            name="allowed_pages",
        ),
        migrations.AlterField(
            model_name="super_admin",
            name="super_admin_id",
            field=models.CharField(
                blank=True, default="1d2de3ff", max_length=8, unique=True
            ),
        ),
        migrations.AddField(
            model_name="super_admin",
            name="allowed_pages",
            field=models.ManyToManyField(blank=True, to="crm.page"),
        ),
    ]
