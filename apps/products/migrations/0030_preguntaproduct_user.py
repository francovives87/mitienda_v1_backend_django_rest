# Generated by Django 3.2.6 on 2022-05-24 01:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0029_preguntaproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='preguntaproduct',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.user', verbose_name='user'),
            preserve_default=False,
        ),
    ]
