# Generated by Django 3.2.6 on 2022-01-12 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='end_time',
            field=models.IntegerField(default='20', verbose_name='end_time'),
        ),
        migrations.AddField(
            model_name='service',
            name='interval',
            field=models.IntegerField(default='60', verbose_name='interval'),
        ),
        migrations.AddField(
            model_name='service',
            name='start_time',
            field=models.IntegerField(default='9', verbose_name='start_time'),
        ),
    ]