# Generated by Django 5.1 on 2024-09-15 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0019_alter_subscription_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='duration_choice',
            field=models.CharField(blank=True, choices=[('monthly', 'Monthly'), ('semestrial', 'Semestrial'), ('yearly', 'Yearly')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='start_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('pending', 'Pending'), ('paused', 'Paused'), ('cancelled', 'Cancelled'), ('expired', 'Expired')], default='pending', max_length=100),
        ),
    ]
