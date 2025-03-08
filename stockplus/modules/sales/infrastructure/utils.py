"""
Utility functions for the sales module.
"""

import datetime
import random
from typing import Optional

from stockplus.modules.sales.infrastructure.models import Sale, Invoice


def generate_invoice_number(company_id: int) -> str:
    """
    Generate a unique invoice number.
    
    Args:
        company_id: The ID of the company to include in the invoice number.
        
    Returns:
        A unique invoice number.
    """
    # Format: INV-{YEAR}{MONTH}-{COMPANY_ID}-{RANDOM_DIGITS}
    # Example: INV-202503-123-4567
    
    now = datetime.datetime.now()
    year_month = now.strftime("%Y%m")
    random_digits = ''.join(str(random.randint(0, 9)) for _ in range(4))
    
    invoice_number = f"INV-{year_month}-{company_id}-{random_digits}"
    
    # Check if this invoice number already exists
    if Invoice.objects.filter(invoice_number=invoice_number).exists():
        # Try again with a different random number
        return generate_invoice_number(company_id)
    
    return invoice_number


def generate_pdf_invoice(invoice_id: int) -> Optional[str]:
    """
    Generate a PDF invoice.
    
    Args:
        invoice_id: The ID of the invoice to generate a PDF for.
        
    Returns:
        The path to the generated PDF, or None if the invoice is not found.
    """
    try:
        invoice = Invoice.objects.get(id=invoice_id)
    except Invoice.DoesNotExist:
        return None
    
    # TODO: Implement PDF generation using a library like ReportLab or WeasyPrint
    # For now, we'll just return a placeholder
    
    return f"/tmp/invoice_{invoice.invoice_number}.pdf"
