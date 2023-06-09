# Generated by Django 4.1.3 on 2023-03-23 07:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('webscraper', '0002_brand_website_alter_product_name_productoffer_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='productoffer',
            name='product',
        ),
        migrations.AddField(
            model_name='productoffer',
            name='brand',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productoffer',
            name='name',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='productoffer',
            name='website',
            field=models.CharField(max_length=100),
        ),
        migrations.DeleteModel(
            name='Brand',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.DeleteModel(
            name='Website',
        ),
    ]
