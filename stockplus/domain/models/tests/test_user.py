"""
Tests for the User domain model.
"""

import unittest
from datetime import date

from stockplus.domain.models.user import User


class TestUser(unittest.TestCase):
    """
    Test case for the User domain model.
    """
    
    def test_fullname(self):
        """
        Test the fullname property.
        """
        # Given
        user = User(first_name="John", last_name="Doe")
        
        # When
        fullname = user.fullname
        
        # Then
        self.assertEqual(fullname, "John Doe")
    
    def test_fullname_with_empty_first_name(self):
        """
        Test the fullname property with an empty first name.
        """
        # Given
        user = User(first_name="", last_name="Doe")
        
        # When
        fullname = user.fullname
        
        # Then
        self.assertEqual(fullname, "Doe")
    
    def test_fullname_with_empty_last_name(self):
        """
        Test the fullname property with an empty last name.
        """
        # Given
        user = User(first_name="John", last_name="")
        
        # When
        fullname = user.fullname
        
        # Then
        self.assertEqual(fullname, "John")
    
    def test_fullname_with_empty_names(self):
        """
        Test the fullname property with empty names.
        """
        # Given
        user = User(first_name="", last_name="")
        
        # When
        fullname = user.fullname
        
        # Then
        self.assertEqual(fullname, "")
    
    def test_verify(self):
        """
        Test the verify method.
        """
        # Given
        user = User(is_verified=False)
        
        # When
        user.verify()
        
        # Then
        self.assertTrue(user.is_verified)
    
    def test_deactivate(self):
        """
        Test the deactivate method.
        """
        # Given
        user = User(is_active=True)
        
        # When
        user.deactivate()
        
        # Then
        self.assertFalse(user.is_active)
    
    def test_activate(self):
        """
        Test the activate method.
        """
        # Given
        user = User(is_active=False)
        
        # When
        user.activate()
        
        # Then
        self.assertTrue(user.is_active)
    
    def test_update_profile(self):
        """
        Test the update_profile method.
        """
        # Given
        user = User(
            first_name="John",
            last_name="Doe",
            date_of_birth=date(1990, 1, 1)
        )
        
        # When
        user.update_profile(
            first_name="Jane",
            last_name="Smith",
            date_of_birth=date(1995, 5, 5)
        )
        
        # Then
        self.assertEqual(user.first_name, "Jane")
        self.assertEqual(user.last_name, "Smith")
        self.assertEqual(user.date_of_birth, date(1995, 5, 5))
    
    def test_update_profile_partial(self):
        """
        Test the update_profile method with partial updates.
        """
        # Given
        user = User(
            first_name="John",
            last_name="Doe",
            date_of_birth=date(1990, 1, 1)
        )
        
        # When
        user.update_profile(first_name="Jane")
        
        # Then
        self.assertEqual(user.first_name, "Jane")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.date_of_birth, date(1990, 1, 1))
    
    def test_assign_to_company(self):
        """
        Test the assign_to_company method.
        """
        # Given
        user = User()
        
        # When
        user.assign_to_company(company_id=1, role="manager")
        
        # Then
        self.assertEqual(user.company_id, 1)
        self.assertEqual(user.role, "manager")
    
    def test_remove_from_company(self):
        """
        Test the remove_from_company method.
        """
        # Given
        user = User(company_id=1, role="manager")
        
        # When
        user.remove_from_company()
        
        # Then
        self.assertIsNone(user.company_id)
        self.assertIsNone(user.role)


if __name__ == '__main__':
    unittest.main()
