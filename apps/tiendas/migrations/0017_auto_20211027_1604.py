# Generated by Django 3.2.6 on 2021-10-27 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tiendas', '0016_auto_20211026_1731'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slider',
            name='text',
        ),
        migrations.RemoveField(
            model_name='slider',
            name='title',
        ),
    ]
