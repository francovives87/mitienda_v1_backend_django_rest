# Generated by Django 3.2.6 on 2022-08-23 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0033_preguntaproduct_visto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='category_product', verbose_name='Imagen'),
        ),
    ]
