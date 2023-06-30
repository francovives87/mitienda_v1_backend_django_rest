# Generated by Django 3.2.6 on 2021-10-19 05:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0002_auto_20211019_0232'),
        ('tiendas', '0003_auto_20211019_0210'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('personal_user_data', models.IntegerField(blank=True, null=True, verbose_name='personal_user_data')),
                ('notas', models.CharField(blank=True, max_length=255, null=True, verbose_name='Notas')),
                ('total', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Total')),
                ('estado', models.CharField(default='en espera', max_length=15, verbose_name='estado')),
                ('metodo_pago', models.CharField(default='efectivo', max_length=20, verbose_name='Metodo de pago')),
                ('quantity_products', models.PositiveIntegerField(verbose_name='cantidad de productos')),
                ('tienda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tiendas.tienda', verbose_name='tienda_orders')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Usuario', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Orden',
                'verbose_name_plural': 'Ordenes',
            },
        ),
        migrations.CreateModel(
            name='Order_detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('quantity', models.PositiveIntegerField(verbose_name='cantidad')),
                ('price_sale', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Precion_venta')),
                ('price_off', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Precion_en_oferta')),
                ('variacion_id', models.IntegerField(blank=True, null=True, verbose_name='Variacion_id')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Orden', to='orders.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Producto', to='products.product')),
            ],
            options={
                'verbose_name': 'Orden Detalle',
                'verbose_name_plural': 'Ordenes Detalles',
            },
        ),
    ]
