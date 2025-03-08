from django.contrib.auth import get_user_model

User = get_user_model()

def add_users_to_subscription_group(subscription):
    """
    Add users to a subscription group.
    
    Args:
        subscription: The subscription to add users to.
    """
    from stockplus.modules.subscription.infrastructure.models import SubscriptionPlan

    subscription_plan_obj = subscription.subscription_plan
    # Filter active subscriptions plan, excluding the one related to the user current subscription
    subs_plan_qs = SubscriptionPlan.objects.filter(active=True).exclude(id=subscription_plan_obj.id)
    subs_groups = subs_plan_qs.values_list('group_id', flat=True)
    subs_groups_set = set(subs_groups)

    # Group associated to the current subscription
    group = subscription_plan_obj.group
    group_id = group.id

    if hasattr(subscription, 'company') and subscription.company:
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
    """
    Remove users from a subscription group.
    
    Args:
        subscription: The subscription to remove users from.
    """
    if hasattr(subscription, 'company') and subscription.company:
        users = User.objects.filter(company=subscription.company)
        for user in users:
            user.groups.remove(subscription.subscription_plan.group)
    else:
        subscription.user.groups.remove(subscription.subscription_plan.group)


def send_expiration_notification(subscription):
    """
    Send a notification to the user that their subscription is about to expire.
    
    Args:
        subscription: The subscription that is about to expire.
    """
    # This is a placeholder for future implementation
    pass
