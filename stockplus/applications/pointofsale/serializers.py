from rest_framework import serializers

from stockplus.models import PointOfSale

class PointOfSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointOfSale
        exclude = ['company']