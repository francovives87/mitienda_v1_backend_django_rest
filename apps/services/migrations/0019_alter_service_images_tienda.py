# Generated by Django 3.2.6 on 2022-04-20 17:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tiendas', '0051_plan_images_x_services'),
        ('services', '0018_service_images_tienda'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service_images',
            name='tienda',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tiendas.tienda', verbose_name='tienda'),
        ),
    ]
