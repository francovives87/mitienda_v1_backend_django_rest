# Generated by Django 3.2.6 on 2021-11-23 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiendas', '0022_alter_tienda_plan'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='images_x_entries',
            field=models.IntegerField(default=4, verbose_name='imagenes_x_entrada'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plan',
            name='images_x_products',
            field=models.IntegerField(default=4, verbose_name='imagenes_x_producto'),
            preserve_default=False,
        ),
    ]
