# Generated by Django 3.2.6 on 2022-04-20 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0019_alter_service_images_tienda'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='service_images',
            options={'verbose_name': 'Imagen de producto', 'verbose_name_plural': 'Mas Imagenes de los productos'},
        ),
        migrations.AddField(
            model_name='service',
            name='portada',
            field=models.BooleanField(default=False, verbose_name='Destacado'),
        ),
    ]
