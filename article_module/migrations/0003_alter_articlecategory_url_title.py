# Generated by Django 4.1.6 on 2023-06-03 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article_module', '0002_alter_articlecategory_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlecategory',
            name='url_title',
            field=models.CharField(max_length=200, unique=True, verbose_name='عنوان در url'),
        ),
    ]
