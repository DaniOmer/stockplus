from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from builder.applications.user.serializers import UserProfileSerializer

User = get_user_model()

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint to retrieve or update User
    """
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Optionally restricts the returned user details by
        filtering against the 'id' query parameter in the URL.
        """
        user_id = self.kwargs.get('pk')
        return self.queryset.filter(id=user_id)
    

    def update(self, request, *args, **kwargs):
        if not request.user.is_staff and request.user != self.get_object():
            return Response(
                {"detail": "You do not have permission to update this profile."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().update(request, *args, **kwargs)
