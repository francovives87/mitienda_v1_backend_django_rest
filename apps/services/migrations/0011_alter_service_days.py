# Generated by Django 3.2.6 on 2022-01-19 20:18

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0010_alter_service_days'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='days',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), blank=True, size=None),
        ),
    ]
