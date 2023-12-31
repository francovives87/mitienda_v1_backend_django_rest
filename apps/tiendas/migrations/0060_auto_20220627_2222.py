# Generated by Django 3.2.6 on 2022-06-28 01:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tiendas', '0059_auto_20220627_2215'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='title_font',
            options={'verbose_name': 'fuente_titulo', 'verbose_name_plural': 'fuentes titulo'},
        ),
        migrations.RemoveField(
            model_name='title_font',
            name='tienda',
        ),
        migrations.AddField(
            model_name='colors',
            name='font_title',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tiendas.title_font', verbose_name='fuente_titulo'),
        ),
    ]
