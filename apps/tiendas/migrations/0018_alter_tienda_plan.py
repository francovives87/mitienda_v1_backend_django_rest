# Generated by Django 3.2.6 on 2021-11-03 20:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tiendas', '0017_auto_20211027_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tienda',
            name='plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tiendas.plan', verbose_name='Plan'),
        ),
    ]