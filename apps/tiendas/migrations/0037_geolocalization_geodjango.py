# Generated by Django 3.2.6 on 2022-03-18 21:42

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tiendas', '0036_auto_20220317_1907'),
    ]

    operations = [
        migrations.CreateModel(
            name='Geolocalization_geodjango',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tienda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tiendas.tienda', verbose_name='tienda')),
            ],
        ),
    ]
