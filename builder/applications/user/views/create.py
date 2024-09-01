from django.contrib.auth import get_user_model
from rest_framework import permissions, generics

from builder.applications.user.serializers import UserSerializer

User = get_user_model()

class UserCreateView(generics.CreateAPIView):
    """
    API endpoint to create User
    """
    serializer_class = UserSerializer
    permission_classes =[permissions.AllowAny]
