# Generated by Django 5.1 on 2025-03-09 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_invitation_table_alter_notification_table_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='notification',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='notification',
            name='type',
            field=models.CharField(choices=[('info', 'Info'), ('warning', 'Warning'), ('error', 'Error'), ('success', 'Success')], default='info', max_length=10),
        ),
    ]
