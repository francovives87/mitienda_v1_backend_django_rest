# Generated by Django 3.2.6 on 2021-10-25 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiendas', '0011_tienda_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tienda',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='logo', verbose_name='logo'),
        ),
    ]
