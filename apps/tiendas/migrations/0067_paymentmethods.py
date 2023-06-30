# Generated by Django 3.2.6 on 2022-10-20 01:35

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tiendas', '0066_auto_20220708_0415'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentMethods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('only_order', models.BooleanField(default=False, verbose_name='solo_ordenar')),
                ('transfer', models.BooleanField(default=False, verbose_name='transferencia')),
                ('mercadopago', models.BooleanField(default=False, verbose_name='mercadopago')),
                ('tienda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tiendas.tienda', verbose_name='tienda')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]