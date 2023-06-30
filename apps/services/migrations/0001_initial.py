# Generated by Django 3.2.6 on 2022-01-10 19:54

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tiendas', '0032_alter_favoritos_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=200, verbose_name='Titulo')),
                ('description', models.TextField(verbose_name='Descripcion:')),
                ('public', models.BooleanField(default=False, verbose_name='publico')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Precio')),
                ('tienda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tiendas.tienda', verbose_name='tienda_service')),
            ],
            options={
                'verbose_name': 'Servicio',
                'verbose_name_plural': 'Servicios',
            },
        ),
    ]
