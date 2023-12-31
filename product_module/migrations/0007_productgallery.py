# Generated by Django 4.2.5 on 2023-09-24 07:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0006_productvisit'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/product_gallery', verbose_name='تصویر')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product_module.product', verbose_name='محصول')),
            ],
            options={
                'verbose_name': 'تصویر گالری',
                'verbose_name_plural': 'گالری تصاویر',
            },
        ),
    ]
