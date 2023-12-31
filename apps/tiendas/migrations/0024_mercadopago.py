# Generated by Django 3.2.6 on 2021-11-24 21:52

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tiendas', '0023_auto_20211123_0010'),
    ]

    operations = [
        migrations.CreateModel(
            name='MercadoPago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('public_key', models.CharField(max_length=150, verbose_name='public_key')),
                ('access_token', models.CharField(max_length=150, verbose_name='access_token')),
                ('tienda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tienda_mercadopago', to='tiendas.tienda', verbose_name='tienda')),
            ],
            options={
                'verbose_name': 'MercadoPago',
                'verbose_name_plural': 'MercadoPago',
            },
        ),
    ]
