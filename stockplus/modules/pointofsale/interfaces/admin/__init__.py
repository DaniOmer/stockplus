from django.contrib import admin

from stockplus.modules.pointofsale.infrastructure.orm.orm import PointOfSaleORM

class PointOfSaleAdmin(admin.ModelAdmin):
    fields = ['name', 'type', 'opening_hours', 'closing_hours', 'collaborators']
    search_fields = ['name', 'type']
