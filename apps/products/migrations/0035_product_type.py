# Generated by Django 3.2.6 on 2022-10-05 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0034_alter_category_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.CharField(default='pdf', max_length=3, verbose_name='Tipo'),
        ),
    ]
