class SubscriptionError(Exception):
    """Base exception for subscription errors."""
    pass


class SubscriptionNotFoundError(SubscriptionError):
    """Exception raised when a subscription is not found."""
    def __init__(self, subscription_id):
        self.subscription_id = subscription_id
        super().__init__(f"Subscription with ID {subscription_id} not found.")


class SubscriptionPlanNotFoundError(SubscriptionError):
    """Exception raised when a subscription plan is not found."""
    def __init__(self, plan_id):
        self.plan_id = plan_id
        super().__init__(f"Subscription plan with ID {plan_id} not found.")


class SubscriptionAlreadyExistsError(SubscriptionError):
    """Exception raised when a user already has a subscription."""
    def __init__(self, user_id):
        self.user_id = user_id
        super().__init__(f"User with ID {user_id} already has a subscription.")


class SubscriptionStatusError(SubscriptionError):
    """Exception raised when a subscription status change is invalid."""
    def __init__(self, subscription_id, current_status, target_status):
        self.subscription_id = subscription_id
        self.current_status = current_status
        self.target_status = target_status
        super().__init__(
            f"Cannot change subscription {subscription_id} from {current_status} to {target_status}."
        )


class SubscriptionLimitExceededError(SubscriptionError):
    """Exception raised when a subscription limit is exceeded."""
    def __init__(self, resource_type, limit, current):
        self.resource_type = resource_type
        self.limit = limit
        self.current = current
        super().__init__(
            f"Subscription limit exceeded for {resource_type}. Limit: {limit}, Current: {current}."
        )
