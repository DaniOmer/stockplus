# Generated by Django 5.1 on 2024-09-30 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0030_alter_subscriptionplan_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionpricing',
            name='stripe_id',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
