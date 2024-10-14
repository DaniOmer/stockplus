# Generated by Django 5.1 on 2024-10-14 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0035_brand_productcategory_product_productfeature'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.RemoveField(
            model_name='productfeature',
            name='product',
        ),
        migrations.RemoveField(
            model_name='productcategory',
            name='parent',
        ),
        migrations.DeleteModel(
            name='Brand',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.DeleteModel(
            name='ProductFeature',
        ),
        migrations.DeleteModel(
            name='ProductCategory',
        ),
    ]
