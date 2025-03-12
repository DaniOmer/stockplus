"""
Company views for the company application.
This module contains the company views for the company application.
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from stockplus.infrastructure.permissions import base_permissions
from stockplus.infrastructure.api.mixins import ResponseFormatterMixin

from stockplus.modules.company.interfaces.serializers import (
    CompanyCreateSerializer,
    CompanyUpdateSerializer,
    CompanyStatusSerializer,
    CompanyPartialUpdateSerializer,
)
from stockplus.modules.company.application.services import CompanyService
from stockplus.modules.company.infrastructure.repositories import CompanyRepository
from stockplus.modules.company.domain.exceptions import (
    CompanyNotFoundException,
)

class CompanyCreateView(ResponseFormatterMixin, generics.CreateAPIView):
    """
    API endpoint to create a company.
    """
    serializer_class = CompanyCreateSerializer
    permission_classes = base_permissions

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.company_service = CompanyService(CompanyRepository())

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.company_service.create_company(serializer.validated_data, request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CompanyDetailView(ResponseFormatterMixin, generics.RetrieveUpdateAPIView):
    """
    API endpoint to retrieve and update a company.
    """
    serializer_class = CompanyUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.company_service = CompanyService(CompanyRepository())

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return CompanyPartialUpdateSerializer
        return CompanyUpdateSerializer
    
    def get_object(self):
        company = CompanyService(CompanyRepository()).get_company_by_id(self.kwargs['pk'])
        if not company:
            raise CompanyNotFoundException()
        return company
    
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=self.get_object(), data=request.data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        self.company_service.update_company(kwargs['pk'], serializer.validated_data)
        updated_company = self.get_object()
        updated_serializer = self.get_serializer(updated_company)
        return Response(updated_serializer.data, status=status.HTTP_200_OK)

class CompanyActivateView(APIView):
    """
    API endpoint to activate a company.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        company_service = CompanyService(
            CompanyRepository(),
        )

        company = company_service.activate_company(pk)
        serializer = CompanyStatusSerializer(company)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CompanyDeactivateView(APIView):
    """
    API endpoint to deactivate a company.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        company_service = CompanyService(
            CompanyRepository(),
        )

        company = company_service.deactivate_company(pk)
        serializer = CompanyStatusSerializer(company)
        return Response(serializer.data, status=status.HTTP_200_OK)