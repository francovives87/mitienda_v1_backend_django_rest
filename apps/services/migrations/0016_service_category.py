# Generated by Django 3.2.6 on 2022-04-19 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0015_category_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='services.category_service', verbose_name='Categoria'),
            preserve_default=False,
        ),
    ]
