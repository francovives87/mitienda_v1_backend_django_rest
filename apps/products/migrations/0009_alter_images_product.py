# Generated by Django 3.2.6 on 2021-11-10 02:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tiendas', '0019_alter_tienda_description'),
        ('products', '0008_remove_product_old_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images_tienda', to='tiendas.tienda', verbose_name='tienda'),
        ),
    ]
