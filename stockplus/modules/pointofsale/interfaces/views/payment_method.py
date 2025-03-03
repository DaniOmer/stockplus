from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from stockplus.modules.pointofsale.application.services import PaymentMethodService
from stockplus.modules.pointofsale.domain.exceptions import (
    PointOfSaleNotFoundError, PaymentMethodNotFoundError
)
from stockplus.modules.pointofsale.interfaces.serializers.pos_payment_method_serializer import PaymentMethodSerializer


class PaymentMethodListCreateView(APIView):
    """
    API view for listing and creating payment methods for a point of sale.
    """
    permission_classes = [IsAuthenticated]
    
    def __init__(self, payment_method_service: PaymentMethodService = None, **kwargs):
        super().__init__(**kwargs)
        self.payment_method_service = payment_method_service
    
    def get(self, request: Request, point_of_sale_id: int) -> Response:
        """
        Get all payment methods for a point of sale.
        
        Args:
            request: The HTTP request.
            point_of_sale_id: The ID of the point of sale.
            
        Returns:
            A response containing the payment methods.
        """
        try:
            payment_methods = self.payment_method_service.get_point_of_sale_payment_methods(point_of_sale_id)
            serialized_payment_methods = [
                PaymentMethodSerializer.from_domain(payment_method)
                for payment_method in payment_methods
            ]
            return Response(serialized_payment_methods, status=status.HTTP_200_OK)
        except PointOfSaleNotFoundError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request: Request, point_of_sale_id: int) -> Response:
        """
        Create a new payment method for a point of sale.
        
        Args:
            request: The HTTP request.
            point_of_sale_id: The ID of the point of sale.
            
        Returns:
            A response containing the created payment method.
        """
        serializer = PaymentMethodSerializer(data={**request.data, "point_of_sale_id": point_of_sale_id})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            payment_method = self.payment_method_service.create_payment_method(
                name=serializer.validated_data["name"],
                point_of_sale_id=point_of_sale_id,
                description=serializer.validated_data.get("description"),
                requires_confirmation=serializer.validated_data.get("requires_confirmation", False),
                confirmation_instructions=serializer.validated_data.get("confirmation_instructions")
            )
            return Response(
                PaymentMethodSerializer.from_domain(payment_method),
                status=status.HTTP_201_CREATED
            )
        except PointOfSaleNotFoundError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


class PaymentMethodRetrieveUpdateDeleteView(APIView):
    """
    API view for retrieving, updating, and deleting a payment method.
    """
    permission_classes = [IsAuthenticated]
    
    def __init__(self, payment_method_service: PaymentMethodService = None, **kwargs):
        super().__init__(**kwargs)
        self.payment_method_service = payment_method_service
    
    def get(self, request: Request, point_of_sale_id: int, payment_method_id: int) -> Response:
        """
        Get a payment method by its ID.
        
        Args:
            request: The HTTP request.
            point_of_sale_id: The ID of the point of sale.
            payment_method_id: The ID of the payment method.
            
        Returns:
            A response containing the payment method.
        """
        try:
            payment_method = self.payment_method_service.get_payment_method(payment_method_id)
            
            # Check if the payment method belongs to the specified point of sale
            if payment_method.point_of_sale_id != point_of_sale_id:
                return Response(
                    {"error": f"Payment method with id {payment_method_id} does not belong to point of sale with id {point_of_sale_id}."},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            return Response(
                PaymentMethodSerializer.from_domain(payment_method),
                status=status.HTTP_200_OK
            )
        except PaymentMethodNotFoundError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request: Request, point_of_sale_id: int, payment_method_id: int) -> Response:
        """
        Update a payment method.
        
        Args:
            request: The HTTP request.
            point_of_sale_id: The ID of the point of sale.
            payment_method_id: The ID of the payment method.
            
        Returns:
            A response containing the updated payment method.
        """
        serializer = PaymentMethodSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # First, get the payment method to check if it belongs to the specified point of sale
            payment_method = self.payment_method_service.get_payment_method(payment_method_id)
            
            if payment_method.point_of_sale_id != point_of_sale_id:
                return Response(
                    {"error": f"Payment method with id {payment_method_id} does not belong to point of sale with id {point_of_sale_id}."},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            updated_payment_method = self.payment_method_service.update_payment_method(
                payment_method_id=payment_method_id,
                name=serializer.validated_data.get("name"),
                description=serializer.validated_data.get("description"),
                requires_confirmation=serializer.validated_data.get("requires_confirmation"),
                confirmation_instructions=serializer.validated_data.get("confirmation_instructions")
            )
            
            return Response(
                PaymentMethodSerializer.from_domain(updated_payment_method),
                status=status.HTTP_200_OK
            )
        except PaymentMethodNotFoundError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request: Request, point_of_sale_id: int, payment_method_id: int) -> Response:
        """
        Delete a payment method.
        
        Args:
            request: The HTTP request.
            point_of_sale_id: The ID of the point of sale.
            payment_method_id: The ID of the payment method.
            
        Returns:
            A response indicating success or failure.
        """
        try:
            # First, get the payment method to check if it belongs to the specified point of sale
            payment_method = self.payment_method_service.get_payment_method(payment_method_id)
            
            if payment_method.point_of_sale_id != point_of_sale_id:
                return Response(
                    {"error": f"Payment method with id {payment_method_id} does not belong to point of sale with id {point_of_sale_id}."},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            self.payment_method_service.delete_payment_method(payment_method_id)
            
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PaymentMethodNotFoundError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


class PaymentMethodToggleStatusView(APIView):
    """
    API view for toggling the active status of a payment method.
    """
    permission_classes = [IsAuthenticated]
    
    def __init__(self, payment_method_service: PaymentMethodService = None, **kwargs):
        super().__init__(**kwargs)
        self.payment_method_service = payment_method_service
    
    def patch(self, request: Request, point_of_sale_id: int, payment_method_id: int) -> Response:
        """
        Toggle the active status of a payment method.
        
        Args:
            request: The HTTP request.
            point_of_sale_id: The ID of the point of sale.
            payment_method_id: The ID of the payment method.
            
        Returns:
            A response containing the updated payment method.
        """
        try:
            # First, get the payment method to check if it belongs to the specified point of sale
            payment_method = self.payment_method_service.get_payment_method(payment_method_id)
            
            if payment_method.point_of_sale_id != point_of_sale_id:
                return Response(
                    {"error": f"Payment method with id {payment_method_id} does not belong to point of sale with id {point_of_sale_id}."},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            updated_payment_method = self.payment_method_service.toggle_payment_method_status(payment_method_id)
            
            return Response(
                PaymentMethodSerializer.from_domain(updated_payment_method),
                status=status.HTTP_200_OK
            )
        except PaymentMethodNotFoundError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
