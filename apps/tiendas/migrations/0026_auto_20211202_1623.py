# Generated by Django 3.2.6 on 2021-12-02 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiendas', '0025_informacion_whatsapp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='informacion',
            name='dias_habiles',
        ),
        migrations.RemoveField(
            model_name='informacion',
            name='horario',
        ),
        migrations.AddField(
            model_name='informacion',
            name='dias_horarios',
            field=models.TextField(blank=True, default='De 09:00 a 13:00 y 15:00 a 19:00', null=True, verbose_name='horario'),
        ),
    ]
