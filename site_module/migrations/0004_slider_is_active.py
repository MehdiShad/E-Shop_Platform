# Generated by Django 4.1.6 on 2023-06-03 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_module', '0003_slider'),
    ]

    operations = [
        migrations.AddField(
            model_name='slider',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='فعال / غیر فعال'),
        ),
    ]
