# Generated by Django 3.2.6 on 2021-11-17 03:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tiendas', '0021_auto_20211117_0050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tienda',
            name='plan',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tienda_plan', to='tiendas.plan', verbose_name='Plan'),
        ),
    ]
