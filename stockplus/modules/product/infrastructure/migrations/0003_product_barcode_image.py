# Generated by Django 5.1 on 2025-03-08 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_product_barcode_product_low_stock_threshold_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='barcode_image',
            field=models.ImageField(blank=True, help_text='Generated barcode image.', null=True, upload_to='barcodes/'),
        ),
    ]
