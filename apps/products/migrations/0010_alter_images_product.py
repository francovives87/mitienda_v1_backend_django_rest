# Generated by Django 3.2.6 on 2021-11-10 02:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_alter_images_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images_product', to='products.product', verbose_name='producto'),
        ),
    ]
