# Generated by Django 3.2.6 on 2021-12-24 20:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_product_only_attribute'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='only_attribute',
        ),
    ]
