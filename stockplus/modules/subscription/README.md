# Subscription Module

This module handles subscription management for StockPlus.

## Features

- Subscription plans (Starter, Premium)
- Subscription creation and management
- Payment processing via Stripe
- Automatic Point of Sale limit enforcement
- Subscription expiry notifications
- Payment history tracking

## Architecture

The subscription module follows a clean architecture approach:

- **Domain Layer**: Contains the core business logic and entities
- **Application Layer**: Contains the services that orchestrate the business logic
- **Infrastructure Layer**: Contains the implementation details (models, repositories)
- **Interface Layer**: Contains the API endpoints and serializers

## API Endpoints

### Subscription Plans

- `GET /api/subscription/plan/`: List all active subscription plans

### Subscriptions

- `GET /api/subscription/`: Get the current user's subscription
- `POST /api/subscription/subscribe/`: Subscribe to a plan
- `POST /api/subscription/cancel/`: Cancel the current subscription
- `POST /api/subscription/change-plan/`: Change the subscription plan
- `GET /api/subscription/payment-history/`: Get the payment history

## Models

### SubscriptionPlan

Represents a subscription plan (e.g., Starter, Premium).

- `name`: The name of the plan
- `description`: The description of the plan
- `active`: Whether the plan is active
- `features`: The features included in the plan
- `pricing`: The pricing options for the plan

### Subscription

Represents a user's subscription.

- `user`: The user who owns the subscription
- `company`: The company the subscription is for
- `subscription_plan`: The subscription plan
- `interval`: The billing interval (month, semester, year)
- `start_date`: The start date of the subscription
- `end_date`: The end date of the subscription
- `renewal_date`: The renewal date of the subscription
- `status`: The status of the subscription (pending, active, cancelled, expired)

## Services

### SubscriptionService

Handles subscription-related operations.

- `get_subscription_plans()`: Get all active subscription plans
- `get_subscription_plan(plan_id)`: Get a subscription plan by ID
- `get_user_subscription(user_id)`: Get a user's subscription
- `create_subscription(user, company, subscription_plan, interval)`: Create a subscription
- `activate_subscription(subscription_id)`: Activate a subscription
- `cancel_subscription(subscription_id)`: Cancel a subscription
- `change_subscription_plan(subscription_id, new_plan_id)`: Change a subscription plan
- `check_expiring_subscriptions()`: Check for subscriptions that are about to expire
- `get_payment_history(user_id)`: Get a user's payment history

## Management Commands

### check_expiring_subscriptions

Checks for subscriptions that are about to expire and sends notifications.

```bash
python manage.py check_expiring_subscriptions
```

## Testing

The subscription module includes comprehensive tests for both the service layer and the API endpoints.

- `test_subscription_service.py`: Tests for the subscription service
- `test_subscription_views.py`: Tests for the subscription views

## Production Readiness

The subscription module is production-ready with the following features:

- **Error Handling**: Comprehensive error handling with detailed logging
- **Transaction Support**: Database transactions for critical operations
- **Logging**: Detailed logging for debugging and monitoring
- **Sentry Integration**: Error tracking with Sentry
- **Rate Limiting**: API rate limiting to prevent abuse
- **Input Validation**: Thorough input validation with clear error messages
- **Testing**: Comprehensive unit and integration tests
- **Documentation**: Detailed API documentation with Swagger
