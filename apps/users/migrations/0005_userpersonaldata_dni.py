# Generated by Django 3.2.6 on 2022-12-07 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_visitor_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpersonaldata',
            name='dni',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='telefono'),
        ),
    ]
