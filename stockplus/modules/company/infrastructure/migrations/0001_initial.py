# Generated by Django 5.1 on 2025-03-07 12:19

import django_ckeditor_5.fields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
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
                ('denomination', models.CharField(max_length=255)),
                ('since', models.DateField(blank=True, null=True)),
                ('site', models.URLField(blank=True, null=True)),
                ('effective', models.BigIntegerField(blank=True, null=True)),
                ('resume', django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True)),
                ('legal_form', models.CharField(max_length=50)),
                ('registration_number', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('tax_id', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('siren', models.CharField(blank=True, max_length=9, null=True, unique=True)),
                ('siret', models.CharField(blank=True, max_length=14, null=True, unique=True)),
                ('ifu', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('idu', models.CharField(blank=True, max_length=100, null=True, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
