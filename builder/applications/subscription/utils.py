def add_users_to_subscription_group(subscription):
    """Add a user to a subscription group"""
    if subscription.company:
        for user in subscription.company.users.all():
            user.groups.add(subscription.subscription_plan.group)
    else:
        subscription.user.groups.add(subscription.subscription_plan.group)

def remove_users_from_subscription_group(subscription):
    """Removes users from the subscription group"""
    if subscription.company:
        for user in subscription.company.users.all():
            user.groups.remove(subscription.subscription_plan.group)
    else:
        subscription.user.groups.remove(subscription.subscription_plan.group)

def send_expiration_notification(subscription):
    pass