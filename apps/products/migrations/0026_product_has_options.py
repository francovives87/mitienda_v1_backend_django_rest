# Generated by Django 3.2.6 on 2022-01-03 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0025_alter_product_only_attribute'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='has_options',
            field=models.BooleanField(default=False, verbose_name='con opciones'),
        ),
    ]
