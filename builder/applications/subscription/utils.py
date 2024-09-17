from builder.models import User, Subscription

def add_users_to_subscription_group(subscription):
    """Add users to a subscription group."""
    subscription_plan_obj = subscription.subscription_plan
    # Filter active subscriptions, excluding the current one
    subs_qs = Subscription.objects.filter(active=True).exclude(id=subscription.id)
    subs_groups = subs_qs.values_list('subscription_plan__group_id', flat=True)
    subs_groups_set = set(subs_groups)

    # Group associated to the current subscription
    group = subscription_plan_obj.group
    group_id = group.id

    if subscription.company:
        users = User.objects.filter(company=subscription.company)
        for user in users:
            current_user_groups = set(user.groups.all().values_list('id', flat=True))
            # Subtract the groups from active subscriptions
            current_user_groups_set = current_user_groups - subs_groups_set
            # Add the current subscription group
            current_user_groups_set.add(group_id)
            user.groups.set(list(current_user_groups_set))
    else:
        user = subscription.user
        current_user_groups = set(user.groups.all().values_list('id', flat=True))
        # Subtract the groups from active subscriptions
        current_user_groups_set = current_user_groups - subs_groups_set
        # Add the current subscription group
        current_user_groups_set.add(group_id)
        user.groups.set(list(current_user_groups_set))


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