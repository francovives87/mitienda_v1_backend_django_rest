# Generated by Django 3.2.6 on 2021-11-17 03:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tiendas', '0019_alter_tienda_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tienda',
            name='plan',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tiendas.plan', verbose_name='Plan'),
        ),
    ]
