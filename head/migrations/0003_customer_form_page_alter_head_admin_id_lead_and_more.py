# Generated by Django 5.1.2 on 2024-12-11 10:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("head", "0002_head_delete_ind_admindt"),
    ]

    operations = [
        migrations.CreateModel(
            name="Customer",
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
                ("admin_id", models.CharField(blank=True, max_length=100, null=True)),
                ("name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(max_length=15)),
                ("address", models.TextField()),
                ("created_by", models.CharField(blank=True, max_length=100, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("age", models.IntegerField(blank=True, default=0, null=True)),
                (
                    "facebook_id",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=15, null=True),
                ),
                (
                    "source",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("organic_search", "Organic Search"),
                            ("google_ad", "Google Ad"),
                            ("youtube", "YouTube"),
                            ("facebook", "Facebook"),
                            ("instagram", "Instagram"),
                            ("twitter", "Twitter"),
                            ("Self", "Self"),
                        ],
                        default="facebook",
                        help_text="Where Lead found us",
                        max_length=50,
                    ),
                ),
                (
                    "preferred_medium",
                    models.CharField(
                        choices=[
                            ("sms", "SMS"),
                            ("facebook", "Facebook"),
                            ("phone_call", "Phone call"),
                        ],
                        default="facebook",
                        help_text="Lead's preferred social media for communication",
                        max_length=50,
                    ),
                ),
                ("active", models.BooleanField(blank=True, default=False)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("NEW", "New Lead"),
                            ("APPROVED", "Approved"),
                            ("REJECTED", "Rejected"),
                            ("PENDING", "Pending"),
                            ("FOLLOWUP", "Follow-Up"),
                        ],
                        default="NEW",
                        help_text="Lead's status for tracking and communication",
                        max_length=50,
                    ),
                ),
                (
                    "profile_picture",
                    models.ImageField(blank=True, null=True, upload_to=""),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True, null=True)),
                ("date_updated", models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Form",
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
                ("form_id", models.CharField(max_length=255, unique=True)),
                ("name", models.CharField(max_length=255)),
                (
                    "status",
                    models.CharField(
                        blank=True, default="INACTIVE", max_length=50, null=True
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Page",
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
                ("page_id", models.CharField(max_length=255, unique=True)),
                ("name", models.CharField(max_length=255)),
                ("category", models.CharField(blank=True, max_length=255, null=True)),
                ("access_token", models.TextField(default="default_token")),
            ],
        ),
        migrations.AlterField(
            model_name="head",
            name="admin_id",
            field=models.CharField(
                blank=True, default="ab374f3a", max_length=8, unique=True
            ),
        ),
        migrations.CreateModel(
            name="Lead",
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
                ("lead_id", models.CharField(max_length=255, unique=True)),
                ("full_name", models.CharField(default="Unknown", max_length=255)),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("created_time", models.DateTimeField(blank=True, null=True)),
                (
                    "form",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="leads",
                        to="head.form",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="form",
            name="page",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="forms",
                to="head.page",
            ),
        ),
        migrations.CreateModel(
            name="UserProfile",
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
                    "facebook_user_id",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "facebook_access_token",
                    models.CharField(blank=True, max_length=1024, null=True),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to="head.head",
                    ),
                ),
            ],
        ),
    ]
