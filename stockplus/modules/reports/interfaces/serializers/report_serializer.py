"""
Report serializers.
This module contains the serializers for the reports module.
"""

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class DateRangeSerializer(serializers.Serializer):
    """
    Serializer for date range parameters.
    """
    start_date = serializers.DateField(
        required=True,
        help_text=_("Start date for the report (YYYY-MM-DD)")
    )
    end_date = serializers.DateField(
        required=True,
        help_text=_("End date for the report (YYYY-MM-DD)")
    )
    pos_id = serializers.IntegerField(
        required=False,
        help_text=_("Point of sale ID to filter by")
    )

    def validate(self, data):
        """
        Validate that start_date is before end_date.
        """
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError(
                _("Start date must be before end date")
            )
        return data


class SalesReportSerializer(DateRangeSerializer):
    """
    Serializer for sales report parameters.
    """
    pass


class ProductReportSerializer(DateRangeSerializer):
    """
    Serializer for product report parameters.
    """
    pass


class InventoryReportSerializer(serializers.Serializer):
    """
    Serializer for inventory report parameters.
    """
    pos_id = serializers.IntegerField(
        required=False,
        help_text=_("Point of sale ID to filter by")
    )
    low_stock_threshold = serializers.IntegerField(
        required=False,
        default=5,
        help_text=_("Threshold for low stock items")
    )


class ExportDataSerializer(serializers.Serializer):
    """
    Serializer for export data parameters.
    """
    export_type = serializers.ChoiceField(
        choices=['sales', 'inventory', 'products'],
        required=True,
        help_text=_("Type of data to export")
    )
    format = serializers.ChoiceField(
        choices=['csv', 'excel', 'pdf'],
        required=False,
        default='csv',
        help_text=_("Export format")
    )
    start_date = serializers.DateField(
        required=False,
        help_text=_("Start date for the report (YYYY-MM-DD)")
    )
    end_date = serializers.DateField(
        required=False,
        help_text=_("End date for the report (YYYY-MM-DD)")
    )
    pos_id = serializers.IntegerField(
        required=False,
        help_text=_("Point of sale ID to filter by")
    )

    def validate(self, data):
        """
        Validate that start_date and end_date are provided for sales export.
        """
        if data['export_type'] == 'sales':
            if 'start_date' not in data or 'end_date' not in data:
                raise serializers.ValidationError(
                    _("Start date and end date are required for sales export")
                )
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError(
                    _("Start date must be before end date")
                )
        return data


class DashboardDataSerializer(serializers.Serializer):
    """
    Serializer for dashboard data parameters.
    """
    pos_id = serializers.IntegerField(
        required=False,
        help_text=_("Point of sale ID to filter by")
    )
