from django.contrib import admin

class PointOfSaleAdmin(admin.ModelAdmin):
    fields = ['name', 'type', 'opening_hours', 'closing_hours', 'collaborators']
    search_fields = ['name', 'type']
