from rest_framework import generics, serializers

from builder.permissions import base_permissions
from builder.modules.company.interfaces.serializers import CompanySerializer


class CompanyCreateView(generics.CreateAPIView):
    serializer_class = CompanySerializer
    permission_classes = base_permissions

    def perform_create(self, serializer):
        if self.request.user.company is not None:
            raise serializers.ValidationError({"detail": "There's already one company associated to this user."})
        serializer.save()
        company = serializer.instance
        self.request.user.company = company
        self.request.user.save()