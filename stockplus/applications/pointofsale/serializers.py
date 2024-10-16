from rest_framework import serializers

from builder.models import User
from stockplus.models import PointOfSale

class PointOfSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointOfSale
        fields = ['id', 'uid', 'name', 'type', 'opening_hours', 'closing_hours', 'collaborators']
        read_only_fields = ['id', 'uid']

class PointOfSaleAddCollaboratorSerializer(serializers.Serializer):
    email = serializers.CharField()
    
    def validate_collaborator_id(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User does not exist.")
        return value