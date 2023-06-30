# Generated by Django 3.2.6 on 2022-03-19 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiendas', '0037_geolocalization_geodjango'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='geolocalization_geodjango',
            options={'verbose_name': 'Geolozalizacion_geodjango', 'verbose_name_plural': 'Geolocalizaciones_geodjango'},
        ),
        migrations.AddField(
            model_name='geolocalization_geodjango',
            name='barrio',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='barrio'),
        ),
        migrations.AddField(
            model_name='geolocalization_geodjango',
            name='ciudad',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='ciudad'),
        ),
        migrations.AddField(
            model_name='geolocalization_geodjango',
            name='codigo_postal',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='codigo_postal'),
        ),
        migrations.AddField(
            model_name='geolocalization_geodjango',
            name='direccion',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='direccion'),
        ),
        migrations.AddField(
            model_name='geolocalization_geodjango',
            name='pais',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='pais'),
        ),
        migrations.AddField(
            model_name='geolocalization_geodjango',
            name='region',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='region'),
        ),
        migrations.AddField(
            model_name='geolocalization_geodjango',
            name='subregion',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='subregion'),
        ),
    ]