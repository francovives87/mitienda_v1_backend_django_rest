# Generated by Django 3.2.6 on 2022-06-28 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiendas', '0060_auto_20220627_2222'),
    ]

    operations = [
        migrations.AddField(
            model_name='title_font',
            name='css',
            field=models.CharField(default='css', max_length=100, verbose_name='url'),
            preserve_default=False,
        ),
    ]
