from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime

from stockplus.modules.subscription.domain.entities import (
    Feature,
    SubscriptionPlan,
    SubscriptionPricing,
    Subscription
)


class ISubscriptionPlanRepository(ABC):
    """
    Interface for the subscription plan repository.
    """
    @abstractmethod
    def get_by_id(self, plan_id: int) -> Optional[SubscriptionPlan]:
        """
        Get a subscription plan by its ID.
        
        Args:
            plan_id: The ID of the subscription plan to retrieve.
            
        Returns:
            The subscription plan, or None if not found.
        """
        pass
    
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[SubscriptionPlan]:
        """
        Get a subscription plan by its name.
        
        Args:
            name: The name of the subscription plan to retrieve.
            
        Returns:
            The subscription plan, or None if not found.
        """
        pass
    
    @abstractmethod
    def get_all_active(self) -> List[SubscriptionPlan]:
        """
        Get all active subscription plans.
        
        Returns:
            A list of active subscription plans.
        """
        pass
    
    @abstractmethod
    def create(self, plan: SubscriptionPlan) -> SubscriptionPlan:
        """
        Create a new subscription plan.
        
        Args:
            plan: The subscription plan to create.
            
        Returns:
            The created subscription plan.
        """
        pass
    
    @abstractmethod
    def update(self, plan: SubscriptionPlan) -> SubscriptionPlan:
        """
        Update an existing subscription plan.
        
        Args:
            plan: The subscription plan to update.
            
        Returns:
            The updated subscription plan.
        """
        pass
    
    @abstractmethod
    def delete(self, plan_id: int) -> None:
        """
        Delete a subscription plan.
        
        Args:
            plan_id: The ID of the subscription plan to delete.
        """
        pass


class ISubscriptionRepository(ABC):
    """
    Interface for the subscription repository.
    """
    @abstractmethod
    def get_by_id(self, subscription_id: int) -> Optional[Subscription]:
        """
        Get a subscription by its ID.
        
        Args:
            subscription_id: The ID of the subscription to retrieve.
            
        Returns:
            The subscription, or None if not found.
        """
        pass
    
    @abstractmethod
    def get_by_user_id(self, user_id: int) -> Optional[Subscription]:
        """
        Get a subscription by its user ID.
        
        Args:
            user_id: The ID of the user.
            
        Returns:
            The subscription, or None if not found.
        """
        pass
    
    @abstractmethod
    def get_by_company_id(self, company_id: int) -> Optional[Subscription]:
        """
        Get a subscription by its company ID.
        
        Args:
            company_id: The ID of the company.
            
        Returns:
            The subscription, or None if not found.
        """
        pass
    
    @abstractmethod
    def get_expiring_subscriptions(self, date: datetime) -> List[Subscription]:
        """
        Get subscriptions that expire on a specific date.
        
        Args:
            date: The date to check for expiring subscriptions.
            
        Returns:
            A list of subscriptions that expire on the specified date.
        """
        pass
    
    @abstractmethod
    def create(self, subscription: Subscription) -> Subscription:
        """
        Create a new subscription.
        
        Args:
            subscription: The subscription to create.
            
        Returns:
            The created subscription.
        """
        pass
    
    @abstractmethod
    def update(self, subscription: Subscription) -> Subscription:
        """
        Update an existing subscription.
        
        Args:
            subscription: The subscription to update.
            
        Returns:
            The updated subscription.
        """
        pass
    
    @abstractmethod
    def delete(self, subscription_id: int) -> None:
        """
        Delete a subscription.
        
        Args:
            subscription_id: The ID of the subscription to delete.
        """
        pass


class IFeatureRepository(ABC):
    """
    Interface for the feature repository.
    """
    @abstractmethod
    def get_by_id(self, feature_id: int) -> Optional[Feature]:
        """
        Get a feature by its ID.
        
        Args:
            feature_id: The ID of the feature to retrieve.
            
        Returns:
            The feature, or None if not found.
        """
        pass
    
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Feature]:
        """
        Get a feature by its name.
        
        Args:
            name: The name of the feature to retrieve.
            
        Returns:
            The feature, or None if not found.
        """
        pass
    
    @abstractmethod
    def get_all(self) -> List[Feature]:
        """
        Get all features.
        
        Returns:
            A list of all features.
        """
        pass
    
    @abstractmethod
    def create(self, feature: Feature) -> Feature:
        """
        Create a new feature.
        
        Args:
            feature: The feature to create.
            
        Returns:
            The created feature.
        """
        pass
    
    @abstractmethod
    def update(self, feature: Feature) -> Feature:
        """
        Update an existing feature.
        
        Args:
            feature: The feature to update.
            
        Returns:
            The updated feature.
        """
        pass
    
    @abstractmethod
    def delete(self, feature_id: int) -> None:
        """
        Delete a feature.
        
        Args:
            feature_id: The ID of the feature to delete.
        """
        pass


class ISubscriptionPricingRepository(ABC):
    """
    Interface for the subscription pricing repository.
    """
    @abstractmethod
    def get_by_id(self, pricing_id: int) -> Optional[SubscriptionPricing]:
        """
        Get a subscription pricing by its ID.
        
        Args:
            pricing_id: The ID of the subscription pricing to retrieve.
            
        Returns:
            The subscription pricing, or None if not found.
        """
        pass
    
    @abstractmethod
    def get_by_plan_id(self, plan_id: int) -> List[SubscriptionPricing]:
        """
        Get all subscription pricings for a subscription plan.
        
        Args:
            plan_id: The ID of the subscription plan.
            
        Returns:
            A list of subscription pricings for the subscription plan.
        """
        pass
    
    @abstractmethod
    def get_by_plan_id_and_interval(self, plan_id: int, interval: str) -> Optional[SubscriptionPricing]:
        """
        Get a subscription pricing by its plan ID and interval.
        
        Args:
            plan_id: The ID of the subscription plan.
            interval: The interval of the subscription pricing.
            
        Returns:
            The subscription pricing, or None if not found.
        """
        pass
    
    @abstractmethod
    def create(self, pricing: SubscriptionPricing) -> SubscriptionPricing:
        """
        Create a new subscription pricing.
        
        Args:
            pricing: The subscription pricing to create.
            
        Returns:
            The created subscription pricing.
        """
        pass
    
    @abstractmethod
    def update(self, pricing: SubscriptionPricing) -> SubscriptionPricing:
        """
        Update an existing subscription pricing.
        
        Args:
            pricing: The subscription pricing to update.
            
        Returns:
            The updated subscription pricing.
        """
        pass
    
    @abstractmethod
    def delete(self, pricing_id: int) -> None:
        """
        Delete a subscription pricing.
        
        Args:
            pricing_id: The ID of the subscription pricing to delete.
        """
        pass
