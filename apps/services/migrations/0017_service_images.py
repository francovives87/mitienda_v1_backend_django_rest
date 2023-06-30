# Generated by Django 3.2.6 on 2022-04-20 15:29

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0016_service_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service_Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('image', models.ImageField(upload_to='service_more_images', verbose_name='Image')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images_services', to='services.service', verbose_name='Servicio')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
