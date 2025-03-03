# Generated by Django 5.1 on 2025-03-03 16:34

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0037_alter_companyaddress_options_alter_user_options_and_more'),
        ('stockplus', '0008_brand_company_productcategory_company'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='brand',
            options={'verbose_name': 'Brand', 'verbose_name_plural': 'Brands'},
        ),
        migrations.AlterModelOptions(
            name='pointofsale',
            options={'verbose_name': 'Point of Sale', 'verbose_name_plural': 'Points of Sale'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
        migrations.AlterModelOptions(
            name='productcategory',
            options={'verbose_name': 'Product Category', 'verbose_name_plural': 'Product Categories'},
        ),
        migrations.AlterModelOptions(
            name='productfeature',
            options={'verbose_name': 'Product Feature', 'verbose_name_plural': 'Product Features'},
        ),
        migrations.AlterModelOptions(
            name='productvariant',
            options={'verbose_name': 'Product Variant', 'verbose_name_plural': 'Product Variants'},
        ),
        migrations.AddField(
            model_name='product',
            name='point_of_sale',
            field=models.ForeignKey(blank=True, help_text='The point of sale this product belongs to.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pos_products', to='stockplus.pointofsale'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='company',
            field=models.ForeignKey(help_text='The company this brand belongs to.', on_delete=django.db.models.deletion.CASCADE, related_name='company_brands', to='builder.company'),
        ),
        migrations.AlterField(
            model_name='pointofsale',
            name='company',
            field=models.ForeignKey(blank=True, help_text='The company this point of sale belongs to.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company_pos', to='builder.company'),
        ),
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(blank=True, help_text='The brand this product belongs to.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='brand_products', to='stockplus.brand'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, help_text='The category this product belongs to.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_products', to='stockplus.productcategory'),
        ),
        migrations.AlterField(
            model_name='product',
            name='company',
            field=models.ForeignKey(help_text='The company this product belongs to.', on_delete=django.db.models.deletion.CASCADE, related_name='company_products', to='builder.company'),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='company',
            field=models.ForeignKey(help_text='The company this product category belongs to.', on_delete=django.db.models.deletion.CASCADE, related_name='company_product_categories', to='builder.company'),
        ),
        migrations.AlterField(
            model_name='productfeature',
            name='product',
            field=models.ForeignKey(help_text='The product this feature belongs to.', on_delete=django.db.models.deletion.CASCADE, related_name='product_features', to='stockplus.product'),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='product',
            field=models.ForeignKey(help_text='The product this variant belongs to.', on_delete=django.db.models.deletion.CASCADE, related_name='product_variants', to='stockplus.product'),
        ),
        migrations.AlterModelTable(
            name='brand',
            table='stockplus_brand',
        ),
        migrations.AlterModelTable(
            name='pointofsale',
            table='stockplus_pointofsale',
        ),
        migrations.AlterModelTable(
            name='product',
            table='stockplus_product',
        ),
        migrations.AlterModelTable(
            name='productcategory',
            table='stockplus_product_category',
        ),
        migrations.AlterModelTable(
            name='productfeature',
            table='stockplus_product_feature',
        ),
        migrations.AlterModelTable(
            name='productvariant',
            table='stockplus_product_variant',
        ),
        migrations.CreateModel(
            name='PosPaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('logs', models.JSONField(blank=True, default=dict, null=True)),
                ('is_disable', models.BooleanField(default=False, verbose_name='Is disable')),
                ('search', models.TextField(blank=True, db_index=True, null=True)),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('create_by', models.CharField(blank=True, editable=False, max_length=254, null=True, verbose_name='Created by')),
                ('date_update', models.DateTimeField(auto_now=True, verbose_name='Update date')),
                ('update_by', models.CharField(blank=True, editable=False, max_length=254, null=True, verbose_name='Updated by')),
                ('update_count', models.PositiveBigIntegerField(default=0)),
                ('note', models.TextField(blank=True, null=True)),
                ('cache', models.JSONField(blank=True, default=dict, null=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('requires_confirmation', models.BooleanField(default=False)),
                ('confirmation_instructions', models.TextField(blank=True, null=True)),
                ('point_of_sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pos_payment_methods', to='stockplus.pointofsale')),
            ],
            options={
                'verbose_name': 'Payment Method',
                'verbose_name_plural': 'Payment Methods',
                'db_table': 'stockplus_paymentmethod',
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='PointOfSaleProductVariant',
        ),
    ]
