from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0002_subscriptionplan_pos_limit'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionplan',
            name='is_free_trial',
            field=models.BooleanField(default=False, help_text='Indicates if this plan is for free trials.'),
        ),
        migrations.AddField(
            model_name='subscriptionplan',
            name='trial_days',
            field=models.IntegerField(default=30, help_text='Number of days for the free trial period.'),
        ),
    ]
