# Generated by Django 4.1.6 on 2023-06-03 12:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article_module', '0003_alter_articlecategory_url_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlecategory',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='article_module.articlecategory', verbose_name='دسته بندی والد'),
        ),
    ]