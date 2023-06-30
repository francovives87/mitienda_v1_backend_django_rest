# Generated by Django 3.2.6 on 2022-02-03 19:45

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0023_auto_20211227_1829'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_detail',
            name='options',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255, verbose_name='opciones'), blank=True, null=True, size=None),
        ),
    ]
