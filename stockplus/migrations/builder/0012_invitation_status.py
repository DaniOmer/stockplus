# Generated by Django 5.1 on 2024-09-07 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0011_alter_user_username_collaboration'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='status',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('VALIDATED', 'VALIDATED'), ('EXPIRED', 'EXPIRED')], default='PENDING', max_length=50),
        ),
    ]
