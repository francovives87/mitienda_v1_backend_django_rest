# Generated by Django 3.2.6 on 2021-12-24 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiendas', '0028_auto_20211207_0102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tienda',
            name='logo',
            field=models.ImageField(blank=True, default='/defaults/logo_generico.png', null=True, upload_to='logo', verbose_name='logo'),
        ),
    ]
