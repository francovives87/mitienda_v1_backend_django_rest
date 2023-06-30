# Generated by Django 3.2.6 on 2021-11-17 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiendas', '0020_alter_tienda_plan'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='blog_categories',
            field=models.IntegerField(default=1, verbose_name='blog_categories'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plan',
            name='blog_entries',
            field=models.IntegerField(default=1, verbose_name='blog_entries'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plan',
            name='product_categories',
            field=models.IntegerField(default=1, verbose_name='product_categories'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plan',
            name='product_products',
            field=models.IntegerField(default=1, verbose_name='product_products'),
            preserve_default=False,
        ),
    ]