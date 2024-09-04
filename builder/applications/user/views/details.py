from django.contrib.auth import get_user_model

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from builder.models import UserAddress
from builder.permissions import IsSelf
from builder.applications.user.serializers import UserProfileSerializer, UserAddressSerializer

User = get_user_model()

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint to retrieve or update User
    """
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsSelf]

    def get_queryset(self):
        user_id = self.kwargs.get('pk')
        return self.queryset.filter(id=user_id)
    

    def update(self, request, *args, **kwargs):
        if not request.user.is_staff and request.user != self.get_object():
            return Response(
                {"detail": "You do not have permission to update this profile."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().update(request, *args, **kwargs)


class UserAddressDetailsView(generics.RetrieveUpdateAPIView):
    """
    API endpoint to get or update User Address
    """
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer
    permission_classes = [IsAuthenticated, IsSelf]

    def get_queryset(self):
        address_id = self.kwargs.get('pk')
        return self.queryset.filter(id=address_id)
