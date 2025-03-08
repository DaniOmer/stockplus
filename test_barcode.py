"""
Test script to verify barcode image generation for products.
"""

import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuration.settings')
django.setup()

from stockplus.modules.product.infrastructure.models import Product
from stockplus.modules.company.infrastructure.models import Company
from stockplus.modules.address.infrastructure.models import CompanyAddress
from django.contrib.auth import get_user_model

User = get_user_model()

def test_barcode_generation():
    """
    Test barcode generation for a product.
    """
    print("Testing barcode generation...")
    
    # Create a test user if not exists
    user, created = User.objects.get_or_create(
        email="test@example.com",
        defaults={
            "first_name": "Test",
            "last_name": "User",
            "is_active": True,
        }
    )
    
    if created:
        user.set_password("password123")
        user.save()
        print(f"Created test user: {user.email}")
    else:
        print(f"Using existing user: {user.email}")
    
    # Create a test company if not exists
    company, created = Company.objects.get_or_create(
        denomination="Test Company",
        defaults={
            "legal_form": "Individual",
            "is_disable": False,
        }
    )
    
    if created:
        print(f"Created test company: {company.denomination}")
    else:
        print(f"Using existing company: {company.denomination}")
    
    # Skip company address creation as the table might not exist
    print("Skipping company address creation")
    
    # Create a test product
    product = Product.objects.create(
        name=f"Test Product {Product.objects.count() + 1}",
        description="A test product",
        stock=10,
        company=company,
    )
    
    print(f"Created product: {product.name}")
    print(f"Barcode: {product.barcode}")
    
    # Check if barcode image was generated
    if product.barcode_image:
        print(f"Barcode image generated: {product.barcode_image.url}")
    else:
        print("No barcode image was generated.")
    
    return product

if __name__ == "__main__":
    test_barcode_generation()
