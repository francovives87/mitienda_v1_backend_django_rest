# Generated by Django 3.2.6 on 2021-12-24 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_remove_variaciones_no_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='only_attribute',
            field=models.BooleanField(default=False, verbose_name='Solo atributo'),
        ),
    ]
