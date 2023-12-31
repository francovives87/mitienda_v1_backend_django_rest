# Generated by Django 3.2.6 on 2022-05-23 17:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('services', '0020_auto_20220420_1638'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpinionesServices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('rating', models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True, verbose_name='Rating')),
                ('opinion', models.CharField(blank=True, max_length=255, null=True)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.service', verbose_name='producto')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Opinion Producto',
                'verbose_name_plural': 'Opiniones Productos',
            },
        ),
    ]
