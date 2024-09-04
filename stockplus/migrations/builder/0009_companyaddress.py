# Generated by Django 5.1 on 2024-09-04 14:00

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0008_useraddress'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('logs', models.JSONField(blank=True, default=dict, null=True)),
                ('is_disable', models.BooleanField(default=False, editable=False, verbose_name='Is disable')),
                ('search', models.TextField(blank=True, db_index=True, null=True)),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('create_by', models.CharField(blank=True, editable=False, max_length=254, null=True, verbose_name='Created by')),
                ('date_update', models.DateTimeField(auto_now=True, verbose_name='Update date')),
                ('update_by', models.CharField(blank=True, editable=False, max_length=254, null=True, verbose_name='Updated by')),
                ('update_count', models.PositiveBigIntegerField(default=0)),
                ('note', models.TextField(blank=True, null=True)),
                ('cache', models.JSONField(blank=True, default=dict, null=True)),
                ('street', models.CharField(blank=True, max_length=255, null=True)),
                ('complement', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=255, null=True)),
                ('state', models.CharField(blank=True, max_length=255, null=True)),
                ('state_code', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('country_code', models.CharField(blank=True, max_length=255, null=True)),
                ('cedex', models.CharField(blank=True, max_length=255, null=True)),
                ('cedex_code', models.CharField(blank=True, max_length=255, null=True)),
                ('special', models.CharField(blank=True, max_length=255, null=True)),
                ('index', models.CharField(blank=True, max_length=255, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('is_siege', models.BooleanField(default=False)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_address', to='builder.company')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
