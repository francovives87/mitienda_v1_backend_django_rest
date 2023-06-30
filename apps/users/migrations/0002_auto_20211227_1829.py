# Generated by Django 3.2.6 on 2021-12-27 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpersonaldata',
            name='apellido',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='apellido'),
        ),
        migrations.AlterField(
            model_name='userpersonaldata',
            name='ciudad',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='ciudad'),
        ),
        migrations.AlterField(
            model_name='userpersonaldata',
            name='codigo_postal',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='codigo postal'),
        ),
        migrations.AlterField(
            model_name='userpersonaldata',
            name='direccion',
            field=models.CharField(blank=True, max_length=80, null=True, verbose_name='direccion'),
        ),
        migrations.AlterField(
            model_name='userpersonaldata',
            name='estado',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='estado/provincia'),
        ),
        migrations.AlterField(
            model_name='userpersonaldata',
            name='nombre',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='userpersonaldata',
            name='pais',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='pais'),
        ),
        migrations.AlterField(
            model_name='userpersonaldata',
            name='telefono',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='telefono'),
        ),
    ]