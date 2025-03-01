from django.contrib.auth import get_user_model
from rest_framework import permissions, generics, serializers

from builder.models import UserAddress
from builder.modules.user.serializers import UserSerializer, UserAddressSerializer

User = get_user_model()

class UserCreateView(generics.CreateAPIView):
    """
    API endpoint to create User
    """
    serializer_class = UserSerializer
    permission_classes =[permissions.AllowAny]

class UserAddressCreateView(generics.CreateAPIView):
    """
    API endpoint to create User Address
    """
    serializer_class = UserAddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user

        if UserAddress.objects.filter(user=user).exists():
            raise serializers.ValidationError({"detail": "You already have an address."})
        
        serializer.save(user=self.request.user)