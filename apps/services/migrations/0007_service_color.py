# Generated by Django 3.2.6 on 2022-01-13 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0006_alter_booking_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='color',
            field=models.CharField(default='#000000', max_length=7, verbose_name='color'),
        ),
    ]
