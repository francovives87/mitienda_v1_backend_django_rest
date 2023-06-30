# Generated by Django 3.2.6 on 2022-01-20 20:19

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0011_alter_service_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='has_break',
            field=models.BooleanField(default=False, verbose_name='has_break'),
        ),
        migrations.AddField(
            model_name='service',
            name='times_break',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100, verbose_name='times_break'), blank=True, null=True, size=None),
        ),
    ]