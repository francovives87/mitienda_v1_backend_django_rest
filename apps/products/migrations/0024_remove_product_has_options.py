# Generated by Django 3.2.6 on 2022-01-03 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0023_product_has_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='has_options',
        ),
    ]
