from builder.models import User

def add_users_to_subscription_group(subscription):
    """Add a user to a subscription group"""
    if subscription.company:
        users = User.objects.filter(company=subscription.company)
        for user in users:
            user.groups.add(subscription.subscription_plan.group)
    else:
        subscription.user.groups.add(subscription.subscription_plan.group)

def remove_users_from_subscription_group(subscription):
    """Removes users from the subscription group"""
    if subscription.company:
        users = User.objects.filter(company=subscription.company)
        for user in users:
            user.groups.remove(subscription.subscription_plan.group)
    else:
        subscription.user.groups.remove(subscription.subscription_plan.group)

def send_expiration_notification(subscription):
    pass