# Generated by Django 3.2.6 on 2021-12-01 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20211201_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='external_reference',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='external_reference'),
        ),
    ]
