# Generated by Django 3.2.6 on 2021-10-27 21:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_category_blog_short_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category_blog',
            name='short_name',
        ),
    ]