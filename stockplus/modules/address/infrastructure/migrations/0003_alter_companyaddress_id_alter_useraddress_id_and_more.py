# Generated by Django 5.1 on 2025-03-09 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0002_alter_companyaddress_table_alter_useraddress_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyaddress',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterModelTable(
            name='companyaddress',
            table='stockplus_companyaddress',
        ),
        migrations.AlterModelTable(
            name='useraddress',
            table='stockplus_useraddress',
        ),
    ]
