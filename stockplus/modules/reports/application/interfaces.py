"""
Reports application interfaces.
This module contains the interfaces for the reports application services.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import date, datetime
from io import BytesIO


class ReportServiceInterface(ABC):
    """
    Interface for the report service.
    """
    
    @abstractmethod
    def generate_sales_report(
        self, 
        company_id: int, 
        start_date: date, 
        end_date: date, 
        pos_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate a sales report for a specific period.
        
        Args:
            company_id: The ID of the company.
            start_date: The start date of the period.
            end_date: The end date of the period.
            pos_id: Optional point of sale ID to filter by.
            
        Returns:
            A dictionary containing the sales report data.
        """
        pass
    
    @abstractmethod
    def generate_inventory_report(
        self, 
        company_id: int, 
        pos_id: Optional[int] = None,
        low_stock_threshold: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate an inventory report.
        
        Args:
            company_id: The ID of the company.
            pos_id: Optional point of sale ID to filter by.
            low_stock_threshold: Optional threshold for low stock items.
            
        Returns:
            A dictionary containing the inventory report data.
        """
        pass
    
    @abstractmethod
    def generate_product_report(
        self, 
        company_id: int, 
        start_date: date, 
        end_date: date, 
        pos_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate a product performance report for a specific period.
        
        Args:
            company_id: The ID of the company.
            start_date: The start date of the period.
            end_date: The end date of the period.
            pos_id: Optional point of sale ID to filter by.
            
        Returns:
            A dictionary containing the product report data.
        """
        pass


class ExportServiceInterface(ABC):
    """
    Interface for the export service.
    """
    
    @abstractmethod
    def export_sales_data(
        self, 
        company_id: int, 
        start_date: date, 
        end_date: date, 
        format: str = 'csv',
        pos_id: Optional[int] = None
    ) -> BytesIO:
        """
        Export sales data for a specific period.
        
        Args:
            company_id: The ID of the company.
            start_date: The start date of the period.
            end_date: The end date of the period.
            format: The export format ('csv', 'excel', or 'pdf').
            pos_id: Optional point of sale ID to filter by.
            
        Returns:
            A BytesIO object containing the exported data.
        """
        pass
    
    @abstractmethod
    def export_inventory_data(
        self, 
        company_id: int, 
        format: str = 'csv',
        pos_id: Optional[int] = None
    ) -> BytesIO:
        """
        Export inventory data.
        
        Args:
            company_id: The ID of the company.
            format: The export format ('csv', 'excel', or 'pdf').
            pos_id: Optional point of sale ID to filter by.
            
        Returns:
            A BytesIO object containing the exported data.
        """
        pass
    
    @abstractmethod
    def export_product_data(
        self, 
        company_id: int, 
        format: str = 'csv',
        pos_id: Optional[int] = None
    ) -> BytesIO:
        """
        Export product data.
        
        Args:
            company_id: The ID of the company.
            format: The export format ('csv', 'excel', or 'pdf').
            pos_id: Optional point of sale ID to filter by.
            
        Returns:
            A BytesIO object containing the exported data.
        """
        pass


class DashboardServiceInterface(ABC):
    """
    Interface for the dashboard service.
    """
    
    @abstractmethod
    def get_dashboard_data(
        self, 
        company_id: int, 
        pos_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get dashboard data with key performance indicators.
        
        Args:
            company_id: The ID of the company.
            pos_id: Optional point of sale ID to filter by.
            
        Returns:
            A dictionary containing the dashboard data.
        """
        pass
