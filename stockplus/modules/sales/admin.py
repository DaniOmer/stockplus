from django.contrib import admin

from stockplus.modules.sales.infrastructure.models import Sale, SaleItem, Invoice


class SaleItemInline(admin.TabularInline):
    """
    Inline admin for sale items.
    """
    model = SaleItem
    extra = 0
    readonly_fields = ['total_price']


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    """
    Admin for sales.
    """
    list_display = ['id', 'invoice_number', 'date', 'total_amount', 'payment_method', 'point_of_sale', 'is_cancelled']
    list_filter = ['date', 'payment_method', 'is_cancelled', 'point_of_sale']
    search_fields = ['invoice_number', 'notes']
    readonly_fields = ['invoice_number', 'date', 'total_amount', 'is_cancelled', 'cancelled_at', 'cancelled_by']
    inlines = [SaleItemInline]
    date_hierarchy = 'date'


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    """
    Admin for invoices.
    """
    list_display = ['id', 'invoice_number', 'date', 'total_amount', 'is_paid', 'customer_name']
    list_filter = ['date', 'is_paid']
    search_fields = ['invoice_number', 'customer_name', 'customer_email', 'notes']
    readonly_fields = ['invoice_number', 'date', 'total_amount', 'sale', 'net_amount', 'grand_total']
    date_hierarchy = 'date'
