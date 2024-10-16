from django.contrib import admin

from stockplus import models as all_models
from stockplus.applications.pointofsale import admin as admin_pointofsale

@admin.register(all_models.PointOfSale)
class PointOfSaleAdmin(admin_pointofsale.PointOfSaleAdmin): pass