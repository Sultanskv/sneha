# Generated by Django 5.1.2 on 2024-12-11 08:06

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ind_adminDT",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "admin_id",
                    models.CharField(
                        blank=True, default="7bc3dc87", max_length=8, unique=True
                    ),
                ),
                (
                    "admin_name_first",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "admin_name_last",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "admin_email",
                    models.EmailField(blank=True, max_length=254, null=True),
                ),
                (
                    "admin_password",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "admin_phone_number",
                    models.CharField(blank=True, max_length=15, null=True),
                ),
                (
                    "admin_verify_code",
                    models.CharField(blank=True, max_length=15, null=True),
                ),
                ("is_staff", models.BooleanField(default=False)),
            ],
        ),
    ]