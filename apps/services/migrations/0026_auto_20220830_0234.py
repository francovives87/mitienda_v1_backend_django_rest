# Generated by Django 3.2.6 on 2022-08-30 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0025_auto_20220823_0047'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='only_show',
        ),
        migrations.AddField(
            model_name='service',
            name='booking',
            field=models.BooleanField(default=True, verbose_name='booking'),
        ),
    ]