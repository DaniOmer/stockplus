from rest_framework import serializers

from stockplus.modules.user.infrastructure.models.user_model import User
from stockplus.modules.pointofsale.domain.entities import PointOfSale as PointOfSaleDomain
from stockplus.modules.pointofsale.infrastructure.models.pos_model import PointOfSale


class PointOfSaleSerializer(serializers.ModelSerializer):
    """
    Serializer for the point of sale model.
    """
    class Meta:
        model = PointOfSale
        fields = ['id', 'uid', 'name', 'type', 'opening_hours', 'closing_hours', 'collaborators']
        read_only_fields = ['id', 'uid']

    def to_domain(self) -> PointOfSaleDomain:
        """
        Convert the serializer data to a domain model.
        
        Returns:
            A domain model instance.
        """
        validated_data = self.validated_data
        
        # Get collaborator IDs if provided
        collaborator_ids = []
        if 'collaborators' in validated_data:
            collaborator_ids = [c.id for c in validated_data['collaborators']]
        
        return PointOfSaleDomain(
            name=validated_data.get('name', ''),
            type=validated_data.get('type', 'store'),
            opening_hours=validated_data.get('opening_hours'),
            closing_hours=validated_data.get('closing_hours'),
            collaborator_ids=collaborator_ids
        )


class PointOfSaleAddCollaboratorSerializer(serializers.Serializer):
    """
    Serializer for adding a collaborator to a point of sale.
    """
    email = serializers.EmailField()
    
    def validate_email(self, value):
        """
        Validate that the email corresponds to an existing user.
        
        Args:
            value: The email to validate.
            
        Returns:
            The validated email.
            
        Raises:
            ValidationError: If no user with the given email exists.
        """
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User does not exist.")
        return value
    
    def get_collaborator_id(self) -> int:
        """
        Get the ID of the collaborator with the given email.
        
        Returns:
            The ID of the collaborator.
        """
        email = self.validated_data['email']
        return User.objects.get(email=email).id
