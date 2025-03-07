from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionplan',
            name='pos_limit',
            field=models.IntegerField(default=3, help_text='Maximum number of points of sale allowed for this plan. 0 means unlimited.'),
        ),
    ]
