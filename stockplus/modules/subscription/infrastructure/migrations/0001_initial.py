from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('company', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(blank=True, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_disable', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubscriptionPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(blank=True, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_disable', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('active', models.BooleanField(default=True)),
                ('stripe_id', models.CharField(blank=True, max_length=120, null=True)),
                ('features', models.ManyToManyField(related_name='features', to='subscription.feature')),
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
                ('permissions', models.ManyToManyField(limit_choices_to={'codename__in': ['stater', 'premium', 'enterprise'], 'content_type__app_label': 'stockplus'}, related_name='permissions', to='auth.permission')),
            ],
            options={
                'db_table': 'stockplus_subscriptionplan',
                'permissions': [('stater', 'Starter Permissions'), ('premium', 'Premium Permissions'), ('enterprise', 'Enterprise Permissions')],
            },
        ),
        migrations.CreateModel(
            name='SubscriptionPricing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(blank=True, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_disable', models.BooleanField(default=False)),
                ('interval', models.CharField(choices=[('day', 'Day'), ('week', 'Week'), ('month', 'Month'), ('semester', 'Semester'), ('year', 'Year')], default='month', max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(choices=[('eur', 'Euro'), ('usd', 'US Dollar'), ('gbp', 'British Pound'), ('cad', 'Canadian Dollar'), ('aud', 'Australian Dollar'), ('jpy', 'Japanese Yen'), ('cny', 'Chinese Yuan'), ('inr', 'Indian Rupee'), ('brl', 'Brazilian Real'), ('mxn', 'Mexican Peso'), ('zar', 'South African Rand'), ('ngn', 'Nigerian Naira'), ('ghs', 'Ghanaian Cedi'), ('kes', 'Kenyan Shilling'), ('xof', 'CFA Franc BCEAO'), ('xaf', 'CFA Franc BEAC')], default='eur', max_length=10)),
                ('stripe_id', models.CharField(blank=True, max_length=120, null=True)),
                ('subscription_plan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pricing', to='subscription.subscriptionplan')),
            ],
            options={
                'db_table': 'stockplus_subscriptionpricing',
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(blank=True, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_disable', models.BooleanField(default=False)),
                ('interval', models.CharField(choices=[('day', 'Day'), ('week', 'Week'), ('month', 'Month'), ('semester', 'Semester'), ('year', 'Year')], default='month', max_length=100)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('renewal_date', models.DateTimeField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('active', 'Active'), ('expired', 'Expired'), ('cancelled', 'Cancelled')], default='pending', max_length=100)),
                ('company', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='company.company')),
                ('subscription_plan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='subscription.subscriptionplan')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
            options={
                'db_table': 'stockplus_subscription',
            },
        ),
    ]
