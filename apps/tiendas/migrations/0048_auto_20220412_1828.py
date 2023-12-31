# Generated by Django 3.2.6 on 2022-04-12 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiendas', '0047_auto_20220408_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='tienda',
            name='extra_field',
            field=models.CharField(blank=True, max_length=4, null=True, verbose_name='extra_fiel'),
        ),
        migrations.AlterField(
            model_name='colors',
            name='alerts',
            field=models.CharField(blank=True, default='#A463BF', max_length=15, null=True, verbose_name='alerts'),
        ),
        migrations.AlterField(
            model_name='colors',
            name='alerts_font',
            field=models.CharField(blank=True, default='#ffffff', max_length=15, null=True, verbose_name='alerts_fonts'),
        ),
        migrations.AlterField(
            model_name='colors',
            name='bottom_navigation',
            field=models.CharField(default='#A463BF', max_length=15, verbose_name='bottom_navigation'),
        ),
        migrations.AlterField(
            model_name='colors',
            name='info_background_color',
            field=models.CharField(blank=True, default='#A463BF', max_length=15, null=True, verbose_name='info_background_color'),
        ),
        migrations.AlterField(
            model_name='colors',
            name='info_font_color',
            field=models.CharField(blank=True, default='#FFFFFF', max_length=15, null=True, verbose_name='info_font_color'),
        ),
        migrations.AlterField(
            model_name='colors',
            name='info_icons_color',
            field=models.CharField(blank=True, default='#FFFFFF', max_length=15, null=True, verbose_name='info_icons_color'),
        ),
        migrations.AlterField(
            model_name='colors',
            name='navbar',
            field=models.CharField(default='#A463BF', max_length=15, verbose_name='navbar'),
        ),
    ]
