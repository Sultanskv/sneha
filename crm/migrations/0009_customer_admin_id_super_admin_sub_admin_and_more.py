# Generated by Django 5.1.1 on 2024-11-15 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0008_super_admin_facebook_app_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='admin_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='super_admin',
            name='sub_admin',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name='super_admin',
            name='super_admin_id',
            field=models.CharField(blank=True, default='1711008a', max_length=8, unique=True),
        ),
    ]