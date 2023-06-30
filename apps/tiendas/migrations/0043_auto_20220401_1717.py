# Generated by Django 3.2.6 on 2022-04-01 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiendas', '0042_alter_geolocalization_geodjango_tienda'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='bookings',
            field=models.IntegerField(default=0, verbose_name='bookings'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plan',
            name='orders',
            field=models.IntegerField(default=0, verbose_name='ordenes'),
            preserve_default=False,
        ),
    ]
