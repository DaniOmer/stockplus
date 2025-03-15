"""
Repository implementation for the user domain.
This module contains the Django ORM implementation of the user repository.
"""

from typing import Optional, Dict, Any, List
from django.db import transaction
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password

from stockplus.modules.user.domain.entities.user import User
from stockplus.modules.user.application.interfaces import IUserRepository
from stockplus.modules.user.domain.exceptions import ValidationException
UserORM = get_user_model()

class UserRepository(IUserRepository):
    """
    Django ORM implementation of the user repository.
    Implements CRUD operations for User domain entities.
    """

    def get_all(self, raw: bool = False) -> List[User]:
        """
        Get all users.
        """
        users = UserORM.objects.all()
        return [self._to_domain(user) for user in users] if raw else users

    def get_by_id(self, user_id: int, raw: bool = False) -> Optional[User]:
        return self._get_user_by(id=user_id, raw=raw)

    def get_by_email(self, email: str, raw: bool = False) -> Optional[User]:
        return self._get_user_by(email=email, raw=raw)

    def get_by_phone_number(self, phone_number: str, raw: bool = False) -> Optional[User]:
        return self._get_user_by(phone_number=phone_number, raw=raw)

    def get_by_username(self, username: str, raw: bool = False) -> Optional[User]:
        return self._get_user_by(username=username, raw=raw)

    def get_by_company_id(self, company_id: int, raw: bool = False) -> List[User]:
        try:
            users = UserORM.objects.filter(company_id=company_id)
            return [self._to_domain(user) for user in users] if raw else users
        except Exception:
            return []

    @transaction.atomic
    def save(self, user: User) -> User:
        user_data = self._create_orm_mapping(user)

        try:
            # Handle password separately to ensure proper hashing
            if hasattr(user, 'password_hash') and user.password_hash:
                user_data["password"] = make_password(user.password_hash)
        
            user_orm, _ = UserORM.objects.update_or_create(
                id=user.id or None,
                defaults=user_data
            )
            return self._to_domain(user_orm)
        except Exception as e:
            print(e)
            raise ValidationException(str(e))
        
    def update_password(self, user_id: int, new_password: str) -> Optional[User]:
        try:
            user_orm = UserORM.objects.get(id=user_id)
            user_orm.password = make_password(new_password)
            user_orm.save(update_fields=['password', 'updated_at'])
            return self._to_domain(user_orm)
        except UserORM.DoesNotExist:
            return None

    def verify_password(self, user_id: int, password: str) -> bool:
        try:
            user_orm = UserORM.objects.get(id=user_id)
            is_valid = check_password(password, user_orm.password)
            if is_valid:
                self._update_last_login(user_orm)
            return is_valid
        except UserORM.DoesNotExist:
            return False
        
    def _update_last_login(self, user_orm: UserORM) -> None:
        user_orm.last_login = timezone.now()
        user_orm.save(update_fields=['last_login'])

    @transaction.atomic
    def delete(self, user_id: int) -> bool:
        deleted, _ = UserORM.objects.filter(id=user_id).delete()
        return deleted > 0
    
    def _get_user_by(self, raw=True, **kwargs: Any) -> Optional[User]:
        try:
            if raw:
                return UserORM.objects.get(**kwargs)
            else:
                return self._to_domain(UserORM.objects.get(**kwargs))
        except (UserORM.DoesNotExist, ValueError, TypeError):
            return None
    
    def _create_orm_mapping(self, user: User) -> Dict[str, Any]:
        return {
            "email": user.email,
            "phone_number": user.phone_number,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_active": user.is_active,
            "is_verified": user.is_verified,
            "company_id": user.company_id,
            "role": user.role,
        }
        
    def _to_domain(self, user_orm: UserORM) -> User:
        return User(
            id=user_orm.id,
            email=user_orm.email,
            phone_number=user_orm.phone_number,
            username=user_orm.username,
            first_name=user_orm.first_name,
            last_name=user_orm.last_name,
            is_active=user_orm.is_active,
            is_verified=user_orm.is_verified,
            company_id=user_orm.company_id,
            role=user_orm.role,
            created_at=user_orm.date_joined,
            updated_at=user_orm.date_joined
        )
