# Generated by Django 4.1.6 on 2023-06-03 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_module', '0004_slider_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slider',
            name='url',
            field=models.URLField(max_length=500, verbose_name='لینک'),
        ),
    ]
