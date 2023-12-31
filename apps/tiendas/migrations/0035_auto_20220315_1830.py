# Generated by Django 3.2.6 on 2022-03-15 21:30

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tiendas', '0034_auto_20220302_1515'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='codigoqr',
            options={'verbose_name': 'Codigo QR', 'verbose_name_plural': 'Codigos QR'},
        ),
        migrations.CreateModel(
            name='Geolocalization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('pais', models.CharField(max_length=150, verbose_name='pais')),
                ('region', models.CharField(max_length=150, verbose_name='region')),
                ('subregion', models.CharField(max_length=150, verbose_name='subregion')),
                ('ciudad', models.CharField(max_length=150, verbose_name='ciudad')),
                ('direccion', models.CharField(max_length=150, verbose_name='direccion')),
                ('codigo_postal', models.CharField(max_length=150, verbose_name='codigo_postal')),
                ('barrio', models.CharField(max_length=150, verbose_name='barrio')),
                ('lat', models.CharField(max_length=150, verbose_name='lat')),
                ('lng', models.CharField(max_length=150, verbose_name='lng')),
                ('tienda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tiendas.tienda', verbose_name='tienda')),
            ],
            options={
                'verbose_name': 'Geolozalizacion',
                'verbose_name_plural': 'Geolocalizaciones',
            },
        ),
    ]
