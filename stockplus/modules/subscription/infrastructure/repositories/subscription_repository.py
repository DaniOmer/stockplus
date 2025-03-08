from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from django.db import transaction
from django.utils import timezone

from stockplus.modules.subscription.application.interfaces import (
    ISubscriptionPlanRepository,
    ISubscriptionRepository,
    IFeatureRepository,
    ISubscriptionPricingRepository
)
from stockplus.modules.subscription.domain.entities import (
    Feature,
    SubscriptionPlan,
    SubscriptionPricing,
    Subscription
)
from stockplus.modules.subscription.domain.exceptions import (
    SubscriptionNotFoundError,
    SubscriptionPlanNotFoundError
)
from stockplus.modules.subscription.infrastructure.models import (
    Feature as FeatureORM,
    SubscriptionPlan as SubscriptionPlanORM,
    SubscriptionPricing as SubscriptionPricingORM,
    Subscription as SubscriptionORM
)


class FeatureRepository(IFeatureRepository):
    """
    Implementation of the feature repository.
    """
    def get_by_id(self, feature_id: int) -> Optional[Feature]:
        """
        Get a feature by its ID.
        
        Args:
            feature_id: The ID of the feature to retrieve.
            
        Returns:
            The feature, or None if not found.
        """
        try:
            feature_orm = FeatureORM.objects.get(id=feature_id)
            return self._to_domain(feature_orm)
        except FeatureORM.DoesNotExist:
            return None
    
    def get_by_name(self, name: str) -> Optional[Feature]:
        """
        Get a feature by its name.
        
        Args:
            name: The name of the feature to retrieve.
            
        Returns:
            The feature, or None if not found.
        """
        try:
            feature_orm = FeatureORM.objects.get(name=name)
            return self._to_domain(feature_orm)
        except FeatureORM.DoesNotExist:
            return None
    
    def get_all(self) -> List[Feature]:
        """
        Get all features.
        
        Returns:
            A list of all features.
        """
        features_orm = FeatureORM.objects.all()
        return [self._to_domain(feature_orm) for feature_orm in features_orm]
    
    def create(self, feature: Feature) -> Feature:
        """
        Create a new feature.
        
        Args:
            feature: The feature to create.
            
        Returns:
            The created feature.
        """
        feature_orm = FeatureORM(
            uid=uuid4() if not feature.uid else feature.uid,
            name=feature.name,
            description=feature.description
        )
        feature_orm.save()
        
        return self._to_domain(feature_orm)
    
    def update(self, feature: Feature) -> Feature:
        """
        Update an existing feature.
        
        Args:
            feature: The feature to update.
            
        Returns:
            The updated feature.
        """
        try:
            feature_orm = FeatureORM.objects.get(id=feature.id)
        except FeatureORM.DoesNotExist:
            raise ValueError(f"Feature with ID {feature.id} not found.")
        
        feature_orm.name = feature.name
        feature_orm.description = feature.description
        feature_orm.save()
        
        return self._to_domain(feature_orm)
    
    def delete(self, feature_id: int) -> None:
        """
        Delete a feature.
        
        Args:
            feature_id: The ID of the feature to delete.
        """
        try:
            feature_orm = FeatureORM.objects.get(id=feature_id)
            feature_orm.delete()
        except FeatureORM.DoesNotExist:
            raise ValueError(f"Feature with ID {feature_id} not found.")
    
    def _to_domain(self, feature_orm: FeatureORM) -> Feature:
        """
        Convert an ORM feature to a domain feature.
        
        Args:
            feature_orm: The ORM feature to convert.
            
        Returns:
            The domain feature.
        """
        return Feature(
            id=feature_orm.id,
            uid=feature_orm.uid,
            name=feature_orm.name,
            description=feature_orm.description,
            is_active=feature_orm.is_active
        )


class SubscriptionPlanRepository(ISubscriptionPlanRepository):
    """
    Implementation of the subscription plan repository.
    """
    def get_by_id(self, plan_id: int) -> Optional[SubscriptionPlan]:
        """
        Get a subscription plan by its ID.
        
        Args:
            plan_id: The ID of the subscription plan to retrieve.
            
        Returns:
            The subscription plan, or None if not found.
        """
        try:
            plan_orm = SubscriptionPlanORM.objects.get(id=plan_id)
            return self._to_domain(plan_orm)
        except SubscriptionPlanORM.DoesNotExist:
            return None
    
    def get_by_name(self, name: str) -> Optional[SubscriptionPlan]:
        """
        Get a subscription plan by its name.
        
        Args:
            name: The name of the subscription plan to retrieve.
            
        Returns:
            The subscription plan, or None if not found.
        """
        try:
            plan_orm = SubscriptionPlanORM.objects.get(name=name)
            return self._to_domain(plan_orm)
        except SubscriptionPlanORM.DoesNotExist:
            return None
    
    def get_all_active(self) -> List[SubscriptionPlan]:
        """
        Get all active subscription plans.
        
        Returns:
            A list of active subscription plans.
        """
        plans_orm = SubscriptionPlanORM.objects.filter(active=True)
        return [self._to_domain(plan_orm) for plan_orm in plans_orm]
    
    @transaction.atomic
    def create(self, plan: SubscriptionPlan) -> SubscriptionPlan:
        """
        Create a new subscription plan.
        
        Args:
            plan: The subscription plan to create.
            
        Returns:
            The created subscription plan.
        """
        plan_orm = SubscriptionPlanORM(
            uid=uuid4() if not plan.uid else plan.uid,
            name=plan.name,
            description=plan.description,
            active=plan.active,
            group=plan.group,
            stripe_id=plan.stripe_id,
            pos_limit=plan.pos_limit,
            is_free_trial=plan.is_free_trial,
            trial_days=plan.trial_days
        )
        plan_orm.save()
        
        # Add features
        if plan.features:
            for feature in plan.features:
                feature_orm = FeatureORM.objects.get(id=feature.id)
                plan_orm.features.add(feature_orm)
        
        # Add permissions
        if plan.permissions:
            for permission in plan.permissions:
                plan_orm.permissions.add(permission)
        
        return self._to_domain(plan_orm)
    
    @transaction.atomic
    def update(self, plan: SubscriptionPlan) -> SubscriptionPlan:
        """
        Update an existing subscription plan.
        
        Args:
            plan: The subscription plan to update.
            
        Returns:
            The updated subscription plan.
        """
        try:
            plan_orm = SubscriptionPlanORM.objects.get(id=plan.id)
        except SubscriptionPlanORM.DoesNotExist:
            raise SubscriptionPlanNotFoundError(plan.id)
        
        plan_orm.name = plan.name
        plan_orm.description = plan.description
        plan_orm.active = plan.active
        plan_orm.group = plan.group
        plan_orm.stripe_id = plan.stripe_id
        plan_orm.pos_limit = plan.pos_limit
        plan_orm.is_free_trial = plan.is_free_trial
        plan_orm.trial_days = plan.trial_days
        plan_orm.save()
        
        # Update features
        if plan.features is not None:
            plan_orm.features.clear()
            for feature in plan.features:
                feature_orm = FeatureORM.objects.get(id=feature.id)
                plan_orm.features.add(feature_orm)
        
        # Update permissions
        if plan.permissions is not None:
            plan_orm.permissions.clear()
            for permission in plan.permissions:
                plan_orm.permissions.add(permission)
        
        return self._to_domain(plan_orm)
    
    def delete(self, plan_id: int) -> None:
        """
        Delete a subscription plan.
        
        Args:
            plan_id: The ID of the subscription plan to delete.
        """
        try:
            plan_orm = SubscriptionPlanORM.objects.get(id=plan_id)
            plan_orm.delete()
        except SubscriptionPlanORM.DoesNotExist:
            raise SubscriptionPlanNotFoundError(plan_id)
    
    def _to_domain(self, plan_orm: SubscriptionPlanORM) -> SubscriptionPlan:
        """
        Convert an ORM subscription plan to a domain subscription plan.
        
        Args:
            plan_orm: The ORM subscription plan to convert.
            
        Returns:
            The domain subscription plan.
        """
        feature_repository = FeatureRepository()
        features = [feature_repository._to_domain(feature_orm) for feature_orm in plan_orm.features.all()]
        
        return SubscriptionPlan(
            id=plan_orm.id,
            uid=plan_orm.uid,
            name=plan_orm.name,
            description=plan_orm.description,
            active=plan_orm.active,
            features=features,
            group=plan_orm.group,
            permissions=list(plan_orm.permissions.all()),
            stripe_id=plan_orm.stripe_id,
            pos_limit=plan_orm.pos_limit,
            is_free_trial=plan_orm.is_free_trial,
            trial_days=plan_orm.trial_days,
            is_active=plan_orm.is_active
        )


class SubscriptionPricingRepository(ISubscriptionPricingRepository):
    """
    Implementation of the subscription pricing repository.
    """
    def get_by_id(self, pricing_id: int) -> Optional[SubscriptionPricing]:
        """
        Get a subscription pricing by its ID.
        
        Args:
            pricing_id: The ID of the subscription pricing to retrieve.
            
        Returns:
            The subscription pricing, or None if not found.
        """
        try:
            pricing_orm = SubscriptionPricingORM.objects.get(id=pricing_id)
            return self._to_domain(pricing_orm)
        except SubscriptionPricingORM.DoesNotExist:
            return None
    
    def get_by_plan_id(self, plan_id: int) -> List[SubscriptionPricing]:
        """
        Get all subscription pricings for a subscription plan.
        
        Args:
            plan_id: The ID of the subscription plan.
            
        Returns:
            A list of subscription pricings for the subscription plan.
        """
        pricings_orm = SubscriptionPricingORM.objects.filter(subscription_plan_id=plan_id)
        return [self._to_domain(pricing_orm) for pricing_orm in pricings_orm]
    
    def get_by_plan_id_and_interval(self, plan_id: int, interval: str) -> Optional[SubscriptionPricing]:
        """
        Get a subscription pricing by its plan ID and interval.
        
        Args:
            plan_id: The ID of the subscription plan.
            interval: The interval of the subscription pricing.
            
        Returns:
            The subscription pricing, or None if not found.
        """
        try:
            pricing_orm = SubscriptionPricingORM.objects.get(
                subscription_plan_id=plan_id,
                interval=interval
            )
            return self._to_domain(pricing_orm)
        except SubscriptionPricingORM.DoesNotExist:
            return None
    
    def create(self, pricing: SubscriptionPricing) -> SubscriptionPricing:
        """
        Create a new subscription pricing.
        
        Args:
            pricing: The subscription pricing to create.
            
        Returns:
            The created subscription pricing.
        """
        pricing_orm = SubscriptionPricingORM(
            uid=uuid4() if not pricing.uid else pricing.uid,
            subscription_plan_id=pricing.subscription_plan_id,
            interval=pricing.interval,
            price=pricing.price,
            currency=pricing.currency,
            stripe_id=pricing.stripe_id
        )
        pricing_orm.save()
        
        return self._to_domain(pricing_orm)
    
    def update(self, pricing: SubscriptionPricing) -> SubscriptionPricing:
        """
        Update an existing subscription pricing.
        
        Args:
            pricing: The subscription pricing to update.
            
        Returns:
            The updated subscription pricing.
        """
        try:
            pricing_orm = SubscriptionPricingORM.objects.get(id=pricing.id)
        except SubscriptionPricingORM.DoesNotExist:
            raise ValueError(f"Subscription pricing with ID {pricing.id} not found.")
        
        pricing_orm.subscription_plan_id = pricing.subscription_plan_id
        pricing_orm.interval = pricing.interval
        pricing_orm.price = pricing.price
        pricing_orm.currency = pricing.currency
        pricing_orm.stripe_id = pricing.stripe_id
        pricing_orm.save()
        
        return self._to_domain(pricing_orm)
    
    def delete(self, pricing_id: int) -> None:
        """
        Delete a subscription pricing.
        
        Args:
            pricing_id: The ID of the subscription pricing to delete.
        """
        try:
            pricing_orm = SubscriptionPricingORM.objects.get(id=pricing_id)
            pricing_orm.delete()
        except SubscriptionPricingORM.DoesNotExist:
            raise ValueError(f"Subscription pricing with ID {pricing_id} not found.")
    
    def _to_domain(self, pricing_orm: SubscriptionPricingORM) -> SubscriptionPricing:
        """
        Convert an ORM subscription pricing to a domain subscription pricing.
        
        Args:
            pricing_orm: The ORM subscription pricing to convert.
            
        Returns:
            The domain subscription pricing.
        """
        return SubscriptionPricing(
            id=pricing_orm.id,
            uid=pricing_orm.uid,
            subscription_plan_id=pricing_orm.subscription_plan_id,
            interval=pricing_orm.interval,
            price=float(pricing_orm.price),
            currency=pricing_orm.currency,
            stripe_id=pricing_orm.stripe_id,
            is_active=pricing_orm.is_active
        )


class SubscriptionRepository(ISubscriptionRepository):
    """
    Implementation of the subscription repository.
    """
    def get_by_id(self, subscription_id: int) -> Optional[Subscription]:
        """
        Get a subscription by its ID.
        
        Args:
            subscription_id: The ID of the subscription to retrieve.
            
        Returns:
            The subscription, or None if not found.
        """
        try:
            subscription_orm = SubscriptionORM.objects.get(id=subscription_id)
            return self._to_domain(subscription_orm)
        except SubscriptionORM.DoesNotExist:
            return None
    
    def get_by_user_id(self, user_id: int) -> Optional[Subscription]:
        """
        Get a subscription by its user ID.
        
        Args:
            user_id: The ID of the user.
            
        Returns:
            The subscription, or None if not found.
        """
        try:
            subscription_orm = SubscriptionORM.objects.get(user_id=user_id)
            return self._to_domain(subscription_orm)
        except SubscriptionORM.DoesNotExist:
            return None
    
    def get_by_company_id(self, company_id: int) -> Optional[Subscription]:
        """
        Get a subscription by its company ID.
        
        Args:
            company_id: The ID of the company.
            
        Returns:
            The subscription, or None if not found.
        """
        try:
            subscription_orm = SubscriptionORM.objects.get(company_id=company_id)
            return self._to_domain(subscription_orm)
        except SubscriptionORM.DoesNotExist:
            return None
    
    def get_expiring_subscriptions(self, date: datetime) -> List[Subscription]:
        """
        Get subscriptions that expire on a specific date.
        
        Args:
            date: The date to check for expiring subscriptions.
            
        Returns:
            A list of subscriptions that expire on the specified date.
        """
        subscriptions_orm = SubscriptionORM.objects.filter(
            end_date__date=date.date(),
            status='active'
        )
        return [self._to_domain(subscription_orm) for subscription_orm in subscriptions_orm]
    
    def create(self, subscription: Subscription) -> Subscription:
        """
        Create a new subscription.
        
        Args:
            subscription: The subscription to create.
            
        Returns:
            The created subscription.
        """
        subscription_orm = SubscriptionORM(
            uid=uuid4() if not subscription.uid else subscription.uid,
            user_id=subscription.user_id,
            subscription_plan_id=subscription.subscription_plan_id,
            interval=subscription.interval,
            start_date=subscription.start_date,
            end_date=subscription.end_date,
            renewal_date=subscription.renewal_date,
            status=subscription.status
        )
        
        # Add company if it exists
        if hasattr(subscription, 'company_id') and subscription.company_id:
            subscription_orm.company_id = subscription.company_id
        
        subscription_orm.save()
        
        return self._to_domain(subscription_orm)
    
    def update(self, subscription: Subscription) -> Subscription:
        """
        Update an existing subscription.
        
        Args:
            subscription: The subscription to update.
            
        Returns:
            The updated subscription.
        """
        try:
            subscription_orm = SubscriptionORM.objects.get(id=subscription.id)
        except SubscriptionORM.DoesNotExist:
            raise SubscriptionNotFoundError(subscription.id)
        
        subscription_orm.user_id = subscription.user_id
        subscription_orm.subscription_plan_id = subscription.subscription_plan_id
        subscription_orm.interval = subscription.interval
        subscription_orm.start_date = subscription.start_date
        subscription_orm.end_date = subscription.end_date
        subscription_orm.renewal_date = subscription.renewal_date
        subscription_orm.status = subscription.status
        
        # Update company if it exists
        if hasattr(subscription, 'company_id') and subscription.company_id:
            subscription_orm.company_id = subscription.company_id
        
        subscription_orm.save()
        
        return self._to_domain(subscription_orm)
    
    def delete(self, subscription_id: int) -> None:
        """
        Delete a subscription.
        
        Args:
            subscription_id: The ID of the subscription to delete.
        """
        try:
            subscription_orm = SubscriptionORM.objects.get(id=subscription_id)
            subscription_orm.delete()
        except SubscriptionORM.DoesNotExist:
            raise SubscriptionNotFoundError(subscription_id)
    
    def _to_domain(self, subscription_orm: SubscriptionORM) -> Subscription:
        """
        Convert an ORM subscription to a domain subscription.
        
        Args:
            subscription_orm: The ORM subscription to convert.
            
        Returns:
            The domain subscription.
        """
        subscription = Subscription(
            id=subscription_orm.id,
            uid=subscription_orm.uid,
            user_id=subscription_orm.user_id,
            subscription_plan_id=subscription_orm.subscription_plan_id,
            interval=subscription_orm.interval,
            start_date=subscription_orm.start_date,
            end_date=subscription_orm.end_date,
            renewal_date=subscription_orm.renewal_date,
            status=subscription_orm.status,
            is_active=subscription_orm.is_active
        )
        
        # Add company if it exists
        if hasattr(subscription_orm, 'company_id') and subscription_orm.company_id:
            subscription.company_id = subscription_orm.company_id
        
        return subscription
