# Generated by Django 3.2.6 on 2021-10-23 18:32

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tiendas', '0003_auto_20211019_0210'),
    ]

    operations = [
        migrations.CreateModel(
            name='Colors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('navbar', models.CharField(default='#212529', max_length=15, verbose_name='navbar')),
                ('navbar_font', models.CharField(blank=True, max_length=15, null=True, verbose_name='navbar_font')),
                ('bottom_navigation', models.CharField(default='#212529', max_length=15, verbose_name='bottom_navigation')),
                ('bottom_navigation_font', models.CharField(blank=True, max_length=15, null=True, verbose_name='bottom_navigation')),
                ('alerts', models.CharField(blank=True, max_length=15, null=True, verbose_name='alerts')),
                ('alerts_font', models.CharField(blank=True, max_length=15, null=True, verbose_name='alerts')),
                ('tienda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tiendas.tienda', verbose_name='tienda')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
