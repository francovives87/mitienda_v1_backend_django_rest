# Generated by Django 3.2.6 on 2022-11-10 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0035_product_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='visits',
            field=models.IntegerField(default=0, verbose_name='visitas'),
        ),
    ]