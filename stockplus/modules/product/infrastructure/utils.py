"""
Utility functions for the product module.
"""

import random
from typing import Optional

from stockplus.modules.product.infrastructure.models import Product
from stockplus.modules.company.infrastructure.models import Company
from stockplus.modules.address.infrastructure.models import CompanyAddress


def calculate_ean13_checksum(digits: str) -> str:
    """
    Calculate the EAN-13 checksum digit.
    
    Args:
        digits: The first 12 digits of the EAN-13 code.
        
    Returns:
        The checksum digit.
    """
    if len(digits) != 12:
        raise ValueError("EAN-13 requires exactly 12 digits to calculate checksum")
    
    # Multiply each digit by 1 or 3 depending on position
    total = sum(int(digit) * (3 if i % 2 else 1) for i, digit in enumerate(digits))
    
    # Calculate the check digit
    check_digit = (10 - (total % 10)) % 10
    
    return str(check_digit)


def generate_ean13_barcode(company_id: int) -> str:
    """
    Generate a unique EAN-13 barcode.
    
    Args:
        company_id: The ID of the company to include in the barcode.
        
    Returns:
        A unique EAN-13 barcode.
    """
    # Use company_id as part of the barcode to ensure uniqueness across companies
    # Format: 2 digits for country code (e.g., 20-29 for internal use)
    # + 5 digits for company_id (padded with zeros)
    # + 5 random digits
    # + 1 check digit
    
    # Get the company
    try:
        company = Company.objects.get(id=company_id)
        
        # Get the company's country from its address
        country = None
        company_address = CompanyAddress.objects.filter(company=company).first()
        if company_address:
            country = company_address.country
        
        # Get the country code for the barcode
        country_code = get_ean_country_code(country)
    except Exception:
        # Default to internal company use if there's an error
        country_code = "29"
    
    company_part = str(company_id).zfill(5)[:5]  # Ensure exactly 5 digits
    
    # Try up to 100 times to generate a unique barcode
    for _ in range(100):
        # Generate 5 random digits
        random_part = ''.join(str(random.randint(0, 9)) for _ in range(5))
        
        # Combine parts to form the first 12 digits
        first_12_digits = country_code + company_part + random_part
        
        # Calculate the check digit
        check_digit = calculate_ean13_checksum(first_12_digits)
        
        # Form the complete EAN-13 barcode
        barcode = first_12_digits + check_digit
        
        # Check if this barcode already exists
        if not Product.objects.filter(barcode=barcode).exists():
            return barcode
    
    # If we couldn't generate a unique barcode after 100 attempts, raise an exception
    raise ValueError("Could not generate a unique EAN-13 barcode after 100 attempts")


def get_ean_country_code(country_name: Optional[str]) -> str:
    """
    Get the EAN country code for a given country name.
    
    Args:
        country_name: The name of the country
        
    Returns:
        A two-digit country code for EAN-13 barcodes
    """
    # Mapping of country names to EAN country codes
    # This is a simplified mapping, a complete mapping would be more extensive
    country_codes = {
        'United States': '00',
        'Canada': '00',
        'France': '30',
        'Germany': '40',
        'United Kingdom': '50',
        'China': '69',
        'Japan': '45',
        'Spain': '84',
        'Italy': '80',
        'Netherlands': '87',
        'Belgium': '54',
        'Switzerland': '76',
        'Portugal': '56',
        'Austria': '90',
        'Australia': '93',
        'New Zealand': '94',
        'Russia': '46',
        'Brazil': '78',
        'Mexico': '75',
        'South Africa': '60',
        'India': '89',
        # Add more countries as needed
    }
    
    # Default to internal company use if country not found or None
    if not country_name:
        return "29"
    
    return country_codes.get(country_name, "29")


def validate_ean13_barcode(barcode: str) -> bool:
    """
    Validate an EAN-13 barcode.
    
    Args:
        barcode: The barcode to validate.
        
    Returns:
        True if the barcode is valid, False otherwise.
    """
    if not barcode or len(barcode) != 13 or not barcode.isdigit():
        return False
    
    # Calculate the check digit
    calculated_check_digit = calculate_ean13_checksum(barcode[:12])
    
    # Compare with the provided check digit
    return calculated_check_digit == barcode[12]
