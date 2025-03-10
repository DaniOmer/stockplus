# Generated by Django 5.1 on 2025-03-10 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_alter_brand_id_alter_product_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='brand',
            old_name='date_create',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='brand',
            old_name='date_update',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='date_create',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='date_update',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='productcategory',
            old_name='date_create',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='productcategory',
            old_name='date_update',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='productfeature',
            old_name='date_create',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='productfeature',
            old_name='date_update',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='productvariant',
            old_name='date_create',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='productvariant',
            old_name='date_update',
            new_name='updated_at',
        ),
    ]
