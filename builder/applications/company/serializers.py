from rest_framework import serializers

from builder.models import Company

class CompanySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Company
        exclude = ['owner']