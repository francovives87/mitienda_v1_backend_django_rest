# Generated by Django 3.2.6 on 2021-11-03 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiendas', '0018_alter_tienda_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tienda',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Descripcion'),
        ),
    ]
