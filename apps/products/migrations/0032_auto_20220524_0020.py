# Generated by Django 3.2.6 on 2022-05-24 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0031_auto_20220524_0017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preguntaproduct',
            name='pregunta',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='preguntaproduct',
            name='respuesta',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
